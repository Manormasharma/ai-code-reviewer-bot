import os
from crewai import Agent
from dotenv import load_dotenv

load_dotenv()

class CodeReviewAgents:
    def security_agent(self) -> Agent:
        return Agent(
            role="Senior Security & Vulnerability Auditor",
            goal="Identify OWASP Top 10 risks, exposed API keys, SQL injections, broken auth, or security vulnerabilities in the code diff.",
            backstory="A paranoid cybersecurity expert who scrutinizes every line of code for potential exploits and compliance failures.",
            llm="gemini/gemini-2.5-flash",
            verbose=True
        )

    def performance_agent(self) -> Agent:
        return Agent(
            role="Performance & Scalability Engineer",
            goal="Spot N+1 database queries, memory leaks, unindexed queries, or inefficient synchronous loops in the code diff.",
            backstory="A systems architect obsessed with high-throughput microservices, sub-millisecond latencies, and optimal resource usage.",
            llm="gemini/gemini-2.5-flash",
            verbose=True
        )

    def clean_code_agent(self) -> Agent:
        return Agent(
            role="Clean Code & Architecture Lead",
            goal="Ensure architectural consistency, proper error handling, clear variable naming, and adequate test coverage.",
            backstory="A senior software engineering lead who enforces strict code readability, maintainability, and design patterns.",
            llm="gemini/gemini-2.5-flash",
            verbose=True
        )