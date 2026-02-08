import pandas as pd
import streamlit as st
from llama_index.core import VectorStoreIndex, Document
import os

# --- PHASE 1: CSV 데이터 자동 생성 (기존 데이터 복구) ---
def create_csv_data():
    data = [
        {"page": 3, "section": "1절 일반사항", "content": "저장매체 완전삭제제품은 저장영역의 자료를 완전삭제하여 임의 복구가 불가하도록 조치하는 제품이다. [cite: 17]"},
        {"page": 3, "section": "1절 일반사항", "content": "SSD는 HDD와 달리 자기장 방식이 아니며, 덮어쓰기만으로 삭제를 보장할 수 없다. SATA/NVMe 구분 및 표준 API 준용이 필수적이다. [cite: 20, 21]"},
        {"page": 4, "section": "완전삭제 기준", "content": "HDD의 경우 민감자료는 반드시 3회 이상 덮어쓰기를 수행해야 한다. [cite: 40]"},
        {"page": 8, "section": "2.1.1 SSD 완전삭제", "content": "SSD 완전삭제는 덮어쓰기와 표준삭제명령의 조합으로 구성되어야 하며, 각각 독립적이고 연속적으로 수행되어야 한다. [cite: 129, 133]"},
        {"page": 10, "section": "2.1.2 HDD 완전삭제", "content": "HDD 완전삭제는 섹터 단위로 3회 이상 덮어쓰는 방식을 지원해야 하며, 기본값은 3회이다. [cite: 158, 159]"},
        {"page": 13, "section": "3.1 검증 기능", "content": "제품은 최소 20% 이상의 검증범위로 설정 가능해야 하며, 결과가 보고서에 제시되어야 한다. [cite: 231, 232]"},
        {"page": 14, "section": "4. 감사기록", "content": "삭제 결과보고서는 제품 정보, 대상 매체 정보, 완전삭제 방식 및 결과(횟수/데이터/소요시간)를 포함해야 한다. [cite: 266, 270]"}
    ]
    df = pd.DataFrame(data)
    df.to_csv("processed_rag_data.csv", index=False, encoding='utf-8-sig')
    return df

# 파일이 없으면 생성
if not os.path.exists("processed_rag_data.csv"):
    create_csv_data()

# --- PHASE 2: 스트림릿 UI 및 RAG 엔진 ---
st.set_page_config(page_title="보안요구사항 RAG 데모", layout="wide")
st.title("🛡️ 보안요구사항 RAG 지능형 검색 시스템")

@st.cache_resource
def setup_rag_engine():
    df = pd.read_csv("processed_rag_data.csv")
    documents = [
        Document(text=row['content'], metadata={"page": row['page'], "section": row['section']}) 
        for _, row in df.iterrows()
    ]
    # 실제 운영 시에는 OpenAI API 키가 필요합니다.
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine(similarity_top_k=3)

# 사이드바 구성
with st.sidebar:
    st.header("⚙️ 데이터 관리")
    if st.button("CSV 데이터 다시 생성"):
        create_csv_data()
        st.success("데이터가 성공적으로 업데이트되었습니다!")
    
    st.markdown("---")
    st.write("📊 **분석가 리포트**")
    st.caption("데이터 소스: 저장매체 완전삭제 제품 보안요구사항 V0.0")

# 쿼리 엔진 실행 (API 키 설정 확인 필요)
try:
    query_engine = setup_rag_engine()
    
    if prompt := st.chat_input("예: SSD 완전삭제 방식은?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = query_engine.query(prompt)
            st.markdown(response.response)
            
            # 출처 페이지 메타데이터 추출
            source_pages = list(set([n.metadata['page'] for n in response.source_nodes]))
            st.caption(f"📖 출처: {', '.join([f'p.{p}' for p in source_pages])} (국가용 보안요구사항)")

except Exception as e:
    st.warning("OpenAI API 키를 설정하거나 데이터를 확인해주세요.")
    st.error(f"Error: {e}")
