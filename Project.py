import os
import platform
import subprocess
from graphviz import Digraph
import cohere

# Add Graphviz to PATH explicitly
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

# Set up Cohere API
COHERE_API_KEY = "2g9VwNv1m3H19GZhSshn5BtsaAoPFUH8zscHK23W"  # Replace with your Cohere API key
co = cohere.Client(COHERE_API_KEY)

def generate_steps_from_description(description):
    """
    Use Cohere API to generate workflow steps from a general description.
    """
    try:
        response = co.generate(
            model="command",
            prompt=f"Generate a step-by-step workflow for: {description}. Keep each step concise, with a clear heading only.",
            max_tokens=200,
            temperature=0.5,
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error generating workflow steps: {e}")
        return None

def extract_headings(text):
    """
    Extract the heading (first sentence) from each step.
    """
    steps = text.split("\n")
    headings = []
    for step in steps:
        heading = step.split(":")[0]  # Extract text before the colon
        headings.append(heading.strip())
    return headings

def create_flowchart(workflow_text, output_dir, output_file="flowchart", conclusion="Publish or Start Your Business"):
    """
    Generate a flowchart using Graphviz from workflow text and add a concluding step.
    """
    if not workflow_text:
        print("No workflow steps provided. Cannot generate flowchart.")
        return
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_file)

        # Create the flowchart
        diagram = Digraph(format="png")
        diagram.attr(rankdir="TB", size="10,15", dpi="300")  # Larger canvas and higher DPI
        diagram.attr("node", shape="box", style="rounded,filled", color="lightblue", fontname="Arial", fontsize="12")

        steps = extract_headings(workflow_text)  # Extract only the headings
        previous_step = None

        for idx, step in enumerate(steps, start=1):
            step_id = f"Step_{idx}"
            diagram.node(step_id, step)
            if previous_step:
                diagram.edge(previous_step, step_id)
            previous_step = step_id

        # Add concluding step
        if conclusion:
            conclusion_id = "Conclusion"
            diagram.node(conclusion_id, conclusion)
            if previous_step:
                diagram.edge(previous_step, conclusion_id)

        rendered_path = diagram.render(output_path, view=False)
        output_full_path = os.path.abspath(rendered_path)
        print(f"Flowchart saved to {output_full_path}")

        if platform.system() == "Windows":
            os.startfile(output_full_path)
        elif platform.system() == "Darwin":
            subprocess.run(["open", output_full_path])
        else:
            subprocess.run(["xdg-open", output_full_path])

    except Exception as e:
        print(f"Error creating flowchart: {e}")

def main():
    try:
        result = subprocess.run(["dot", "-V"], capture_output=True, text=True)
        print(f"Graphviz is accessible: {result.stdout.strip()}")
    except FileNotFoundError:
        print("Graphviz 'dot' executable not found. Ensure Graphviz is installed and added to PATH.")
        return

    user_request = input("Describe the process you'd like a flowchart for:\n")
    print("\nGenerating workflow steps...")
    workflow_steps = generate_steps_from_description(user_request)

    if workflow_steps:
        print("\nGenerated Workflow Steps:")
        print(workflow_steps)
        print("\nCreating flowchart...")
        create_flowchart(
            workflow_steps,
            output_dir=r"C:\Users\Jd\OneDrive\Desktop\ML\Project",
            output_file="flowchart",
            conclusion="Publish Your Website or Start Your Business!"
        )
    else:
        print("Failed to generate workflow steps. Please try again.")

if __name__ == "__main__":
    main()
