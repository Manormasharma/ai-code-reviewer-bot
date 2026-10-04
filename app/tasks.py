from crewai import Task, Crew, Process
from app.agents import CodeReviewAgents

def run_code_review_pipeline(code_diff: str) -> str:
    print("🤖 AI Review Pipeline started..")
    agents = CodeReviewAgents()
    security = agents.security_agent()
    performance = agents.performance_agent()
    clean_code = agents.clean_code_agent()

    t_security = Task(
        description=f"Analyze the following code diff for security vulnerabilities:\n\n{code_diff}",
        expected_output="A security audit report highlighting any vulnerabilities or confirming safe code.",
        agent=security
    )

    t_perf = Task(
        description=f"Analyze the following code diff for performance bottlenecks:\n\n{code_diff}",
        expected_output="A performance impact report highlighting resource concerns or optimization suggestions.",
        agent=performance
    )

    t_clean = Task(
        description=f"Synthesize the security findings, performance notes, and code diff into a clean, structured Markdown code review comment with constructive suggestions:\n\n{code_diff}",
        expected_output="A professional, well-formatted Markdown code review ready to post on GitHub.",
        agent=clean_code
    )

    crew = Crew(
        agents=[security, performance, clean_code],
        tasks=[t_security, t_perf, t_clean],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    print("🤖 AI Review Pipeline finished successfully.")
    return str(result)