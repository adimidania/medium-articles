import os
import logging
from typing import TypedDict, List, Dict, Any, Annotated
import arxiv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, END, START
from dotenv import load_dotenv
import time
from datetime import datetime
from pydantic import BaseModel

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ResearchWorkflow")

load_dotenv()

# Define state schema
class ResearchState(TypedDict):
    question: str
    subquestions: List[str]
    results: List[Dict]
    reasoning: str
    report: str

class Subquestions(BaseModel):
    subquestions: List[str]

# Original nodes modified for state management
class DecompositionNode:
    def __init__(self, llm):
        self.llm = llm

    def decompose(self, question: str) -> List[str]:
        logger.info(f"Decomposing question: {question}")
        
        prompt_template = """You are a research assistant. Decompose the following research question into subquestions:
        
        Research Question: {question}
        
        List the subquestions:"""
        prompt = PromptTemplate(template=prompt_template, input_variables=["question"])
        
        logger.info("Sending prompt to LLM for decomposition")
        structured_llm = self.llm.with_structured_output(Subquestions)
        start_time = time.time()
        response = structured_llm.invoke(prompt.format(question=question))
        end_time = time.time()
        logger.info(f"LLM response received in {end_time - start_time:.2f} seconds")
        # the response is now a structured object, we need to turn it into a python list
        subquestions = response.dict()['subquestions']
        
        logger.info(f"Extracted {len(subquestions)} subquestions")
        for i, subq in enumerate(subquestions):
            logger.info(f"  Subquestion {i+1}: {subq}")
        
        return subquestions

class ArxivSearchNode:
    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        logger.info(f"Searching arXiv for: '{query}' (max results: {max_results})")
        
        start_time = time.time()
        search = arxiv.Search(query=query, max_results=max_results)
        results = [{
            'title': result.title,
            'summary': result.summary,
            'authors': [author.name for author in result.authors],
            'published': result.published.strftime("%Y-%m-%d"),
            'link': result.entry_id
        } for result in search.results()]
        end_time = time.time()
        
        logger.info(f"Found {len(results)} results in {end_time - start_time:.2f} seconds")
        for i, res in enumerate(results):
            logger.info(f"  Result {i+1}: {res['title']} ({res['published']})")
        
        return results

class SynthesisNode:
    def __init__(self, llm):
        self.llm = llm

    def synthesize(self, results: List[Dict], reasoning: str) -> str:
        logger.info(f"Synthesizing report from {len(results)} search results")
        
        results_str = "\n".join([f"""Result {i+1}:
Title: {res['title']}
Published: {res['published']}
Authors: {', '.join(res['authors'])}
Link: {res.get('link', 'N/A')}
Summary: {res['summary']}\n""" for i, res in enumerate(results)])
        
        prompt_template = """You are an expert research assistant. Create a report based on:
        
        Internal Reasoning:
        {reasoning}
        
        Search Results:
        {results}
        
        Comprehensive Report:"""
        prompt = PromptTemplate(template=prompt_template, 
                              input_variables=["reasoning", "results"])
        
        logger.info("Sending prompt to LLM for synthesis")
        start_time = time.time()
        response = self.llm.invoke(prompt.format(
            reasoning=reasoning, 
            results=results_str
        )).content
        end_time = time.time()
        
        logger.info(f"Synthesis complete in {end_time - start_time:.2f} seconds")
        logger.info(f"Generated report of {len(response.split())} words")
        
        return response

# LangGraph setup
def create_research_workflow():
    logger.info("Initializing research workflow")
    
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o-mini")
    logger.info(f"Using LLM model: gpt-4o-mini")
    
    decomposer = DecompositionNode(llm)
    searcher = ArxivSearchNode()
    synthesizer = SynthesisNode(llm)

    # Define nodes
    def decompose(state: ResearchState):
        logger.info("==== DECOMPOSITION PHASE ====")
        logger.info(f"Starting decomposition for question: {state['question']}")
        
        subquestions = decomposer.decompose(state["question"])
        
        logger.info("Decomposition complete")
        return {
            "subquestions": subquestions,
            "reasoning": f"Step 1: Decomposed question into subquestions:\n{subquestions}\n"
        }

    def search(state: ResearchState):
        logger.info("==== SEARCH PHASE ====")
        logger.info(f"Starting search for {len(state['subquestions'])} subquestions")
        
        all_results = []
        search_reasoning = []
        
        for i, subq in enumerate(state["subquestions"]):
            logger.info(f"Searching for subquestion {i+1}/{len(state['subquestions'])}: {subq}")
            results = searcher.search(subq)
            all_results.extend(results)
            search_reasoning.append(f"Found {len(results)} results for: {subq}")
        
        logger.info(f"Search complete. Total results: {len(all_results)}")
        
        return {
            "results": all_results,
            "reasoning": state["reasoning"] + "\nStep 2: Search Results:\n" + "\n".join(search_reasoning)
        }

    def synthesize(state: ResearchState):
        logger.info("==== SYNTHESIS PHASE ====")
        logger.info(f"Starting synthesis of {len(state['results'])} search results")
        
        report = synthesizer.synthesize(state["results"], state["reasoning"])
        
        logger.info("Synthesis complete")
        return {
            "report": report,
            "reasoning": state["reasoning"] + "\nStep 3: Synthesized final report"
        }

    # Build graph
    logger.info("Building workflow graph")
    workflow = StateGraph(ResearchState)
    workflow.add_node("decompose", decompose)
    workflow.add_node("search", search)
    workflow.add_node("synthesize", synthesize)

    # Add edges with START and END nodes instead of entry/exit points
    workflow.add_edge(START, "decompose")
    workflow.add_edge("decompose", "search")
    workflow.add_edge("search", "synthesize")
    workflow.add_edge("synthesize", END)
    
    logger.info("Workflow graph built successfully")
    
    return workflow.compile()

# Example usage
if __name__ == '__main__':
    # Set up console logger in addition to file logger
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # Also log to file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_handler = logging.FileHandler(f"research_workflow_{timestamp}.log")
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    logger.info("====== RESEARCH WORKFLOW STARTED ======")
    
    research_question = input("Enter your research question: ") or (
        "What are the latest research discoveries in the field of Agentic AI ?"
    )
    
    logger.info(f"Research question: {research_question}")
    
    start_time = time.time()
    logger.info("Initializing workflow")
    workflow = create_research_workflow()
    
    logger.info("Invoking workflow")
    result = workflow.invoke({
        "question": research_question,
        "subquestions": [],
        "results": [],
        "reasoning": "",
        "report": ""
    })
    end_time = time.time()
    
    logger.info(f"Workflow completed in {end_time - start_time:.2f} seconds")
    
    print("\n\nFINAL REPORT:")
    print(result["report"])
    
    logger.info("====== RESEARCH WORKFLOW COMPLETED ======")
    print(f"\nDetailed log saved to: research_workflow_{timestamp}.log")