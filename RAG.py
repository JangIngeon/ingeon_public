import streamlit as st
import pandas as pd
import os
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# --- [Phase 1] 데이터 생성 로직 (CSV 가공 및 저장) ---
def initialize_data():
    # 보안요구사항 PDF의 핵심 내용을 정형 데이터로 변환 [cite: 17, 40, 129, 158, 231, 266]
    data = [
        {"page": 3, "section": "1절 일반사항", "content": "저장매체 완전삭제제품은 저장영역의 자료를 완전삭제하여 임의 복구가 불가하도록 조치하여 데이터 유출을 차단하는 제품이다. [cite: 17]"},
        {"page": 3, "section": "1절 일반사항", "content": "SSD는 HDD와 달리 자기장 방식이 아니며, 직접 물리적 영역 쓰기가 보장되지 않아 덮어쓰기만으로는 부족하다. SATA/NVMe 표준 API 준용이 필수적이다. [cite: 20, 21]"},
        {"page": 4, "section": "완전삭제 기준", "content": "국가정보보안기본지침에 따라 HDD 내 민감자료는 반드시 3회 이상 덮어쓰기를 수행해야 한다. [cite: 40]"},
        {"page": 8, "section": "2.1.1 SSD 완전삭제", "content": "SSD 완전삭제 방식은 덮어쓰기와 표준삭제명령의 조합으로 구성되어야 하며, 각 방식이 독립적이고 연속적으로 수행되어야 한다. [cite: 129, 133]"},
        {"page": 10, "section": "2.1.2 HDD 완전삭제", "content": "HDD 완전삭제는 섹터 단위로 3회 이상 덮어쓰는 방식을 지원해야 하며, 횟수 기본값은 3회이다. [cite: 158, 159]"},
        {"page": 13, "section": "3.1 검증 기능", "content": "삭제 결과 검증 범위는 최소 20% 이상의 비율로 설정할 수 있어야 하며, 결과보고서에 그 내용이 제시되어야 한다. [cite: 231, 232]"},
        {"page": 14, "section": "4. 감사기록", "content": "삭제 결과보고서에는 제품 정보, 대상 매체 정보(시리얼, 용량 등), 적용된 완전삭제 방식 및 소요 시간이 반드시 포함되어야 한다. "}
    ]
    df = pd.DataFrame(data)
    df.to_csv("processed_rag_data.csv", index=False, encoding='utf-8-sig')
    return df

# --- [Phase 2] 스트림릿 설정 및 RAG 구동 ---
st.set_page_config(page_title="보안요구사항 RAG 시스템", layout="wide")

# API 키 설정 (환경 변수 또는 입력)
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")

if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
    Settings.llm = OpenAI(model="gpt-4o", temperature=0.1)
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

    # 데이터 로드
    if not os.path.exists("processed_rag_data.csv"):
        initialize_data()
    
    df = pd.read_csv("processed_rag_data.csv")
    
    # Document 객체 생성 (메타데이터 포함)
    documents = [
        Document(text=row['content'], metadata={"page": row['page'], "section": row['section']}) 
        for _, row in df.iterrows()
    ]
    
    # 인덱스 구축
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine(similarity_top_k=3)

    st.title("🛡️ 국가용 보안요구사항 지능형 검색 (PoC)")
    st.markdown("---")

    # 채팅 UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("질문을 입력하세요 (예: SSD 삭제 방식은?)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = query_engine.query(prompt)
            st.markdown(response.response)
            
            # 가이드라인 준수: 출처 및 페이지 표기
            source_pages = list(set([n.metadata['page'] for n in response.source_nodes]))
            st.caption(f"📖 근거 문서: 국가용 보안요구사항 V0.0 | 관련 페이지: {', '.join([f'p.{p}' for p in source_pages])}")
            
        st.session_state.messages.append({"role": "assistant", "content": response.response})
else:
    st.warning("사이드바에 OpenAI API Key를 입력해주세요.")
