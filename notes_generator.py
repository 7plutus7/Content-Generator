import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_module_structure(module_name, guidance):
    system_prompt = "You are a curriculum architect. Create a detailed hierarchical breakdown of a Python learning module into submodules and sub-submodules."
    user_prompt = (
        f"Module: {module_name}\n"
        f"Guidance: {guidance}\n\n"
        f"Create a focused, book-friendly hierarchical structure for a 30-40 page PDF book:\n"
        f"1. Break this module into 3-5 SUBMODULES (key topics only)\n"
        f"   - Focus on the most important concepts for a beginner\n"
        f"   - Keep it concise and book-appropriate\n"
        f"2. For each submodule, identify 2-4 SUB-SUBMODULES (essential concepts)\n"
        f"   - Focus on core learning points\n"
        f"   - Ensure content fits in 5-7 pages per module\n\n"
        f"Return as JSON with this structure:\n"
        f"{{\n"
        f"  \"submodules\": [\n"
        f"    {{\n"
        f"      \"name\": \"Submodule name\",\n"
        f"      \"description\": \"Brief description\",\n"
        f"      \"sub_submodules\": [\n"
        f"        {{\n"
        f"          \"name\": \"Sub-submodule name\",\n"
        f"          \"description\": \"What student will learn\"\n"
        f"        }}\n"
        f"      ]\n"
        f"    }}\n"
        f"  ]\n"
        f"}}\n\n"
        f"Make the breakdown logical and comprehensive for a beginner learning Python for ML/AI."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.5
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"⚠️ Structure generation failed: {e}")
        return {"submodules": []}

def generate_sub_submodule_content(module_name, submodule_name, sub_submodule_name, description):
    """Generate detailed content for a specific sub-submodule with visual elements"""
    system_prompt = "You are a friendly Python teacher creating book content for beginners. Write concisely for a PDF book format. Include references to visual elements like tables, diagrams, and images."
    user_prompt = (
        f"Create book-friendly learning content for:\n"
        f"Module: {module_name} > {submodule_name} > {sub_submodule_name}\n"
        f"Description: {description}\n\n"
        f"Generate concise, book-appropriate content with:\n"
        f"1. THEORY:\n"
        f"   - Clear, concise explanation\n"
        f"   - Focus on key concepts\n"
        f"   - Book-friendly language\n\n"
        f"2. VISUAL ELEMENTS:\n"
        f"   - Suggest 1-2 relevant images/diagrams with search terms\n"
        f"   - Suggest 1 comparison table if applicable\n\n"
        f"3. CODE EXAMPLE (1-2 examples max):\n"
        f"   - Short, clear examples\n"
        f"   - Essential code only\n"
        f"   - Brief explanation\n\n"
        f"4. KEY TAKEAWAY:\n"
        f"   - 2-3 bullet points summarizing the concept\n\n"
        f"Return as JSON:\n"
        f"{{\n"
        f"  \"theory\": \"Concise explanation (150-250 words)\",\n"
        f"  \"key_points\": [\"point1\", \"point2\", \"point3\"],\n"
        f"  \"visual_elements\": [\n"
        f"    {{\n"
        f"      \"type\": \"image|diagram|table\",\n"
        f"      \"description\": \"What to show\",\n"
        f"      \"search_query\": \"Image search term for unsplash/pexels\"\n"
        f"    }}\n"
        f"  ],\n"
        f"  \"table_data\": {{\n"
        f"    \"headers\": [\"col1\", \"col2\"],\n"
        f"    \"rows\": [[\"data1\", \"data2\"]],\n"
        f"    \"caption\": \"Table description\"\n"
        f"  }},\n"
        f"  \"code_examples\": [\n"
        f"    {{\n"
        f"      \"title\": \"Example name\",\n"
        f"      \"code\": \"Python code (keep short)\",\n"
        f"      \"explanation\": \"Brief explanation\",\n"
        f"      \"output\": \"Expected result\"\n"
        f"    }}\n"
        f"  ]\n"
        f"}}"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
            max_tokens=2000
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"         ⚠️ Content generation failed: {e}")
        return {"theory": "", "key_points": [], "code_examples": [], "exercises": []}

module_function = [
    {
        "name": "build_module",
        "description": "Create a detailed module for a Python & Data for AI course with examples, exercises, and a quiz.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "overview": {"type": "string"},
                "learning_objectives": {"type": "array", "items": {"type": "string"}},
                "prerequisites": {"type": "array", "items": {"type": "string"}},
                "estimated_duration": {"type": "string"},
                "key_terms": {"type": "array", "items": {"type": "string"}},
                "topics": {"type": "array", "items": {"type": "string"}},
                "detailed_content": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "explanation": {"type": "string"},
                            "code_examples": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "code": {"type": "string"},
                                        "explanation": {"type": "string"},
                                        "expected_output": {"type": "string"}
                                    },
                                    "required": ["title", "code", "explanation"]
                                }
                            }
                        },
                        "required": ["title", "explanation"]
                    }
                },
                "exercises": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "prompt": {"type": "string"},
                            "starter_code": {"type": "string"},
                            "solution_outline": {"type": "string"}
                        },
                        "required": ["prompt"]
                    }
                },
                "resources": {"type": "array", "items": {"type": "string"}},
                "project": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "problem_statement": {"type": "string"},
                        "dataset": {"type": "string"},
                        "milestones": {"type": "array", "items": {"type": "string"}},
                        "rubric": {"type": "array", "items": {"type": "string"}},
                        "extensions": {"type": "array", "items": {"type": "string"}}
                    }
                }
            },
            "required": [
                "name",
                "overview",
                "learning_objectives",
                "detailed_content",
                "exercises",
                "estimated_duration",
                "prerequisites",
                "key_terms"
            ]
        }
    }
]

def generate_module(module_name, guidance, module_num, total_modules):
    print(f"\n📚 Module {module_num}/{total_modules}: {module_name}")
    structure = generate_module_structure(module_name, guidance)
    total_sub_subs = sum(len(sm.get("sub_submodules", [])) for sm in structure.get("submodules", []))
    current = 0
    
    for submodule in structure.get("submodules", []):
        submodule["sub_submodules_content"] = []
        for sub_sub in submodule.get("sub_submodules", []):
            current += 1
            print(f"   [{current}/{total_sub_subs}] {sub_sub['name']}")
            content = generate_sub_submodule_content(
                module_name,
                submodule["name"],
                sub_sub["name"],
                sub_sub["description"]
            )
            sub_sub["content"] = content
    
    system_prompt = "You are a friendly, patient teacher creating a comprehensive Python course for absolute beginners. Create module-level overview and metadata."
    user_prompt = (
        f"Create module overview for: {module_name}\n\n"
        f"Submodules covered:\n{json.dumps([sm['name'] for sm in structure.get('submodules', [])], indent=2)}\n\n"
        f"TONE & APPROACH:\n"
        f"- Write in second person (\"you will learn\", \"let's explore\")\n"
        f"- Be conversational and encouraging, not academic or dry\n"
        f"- Assume ZERO prior knowledge - explain everything from scratch\n"
        f"- Use relatable real-world analogies (cooking, everyday tasks, etc.)\n"
        f"- Include motivational context: \"why should I care about this?\"\n"
        f"- Break down intimidating concepts into digestible chunks\n"
        f"- Acknowledge common student struggles and provide reassurance\n\n"
        f"CONTENT STRUCTURE - Follow this order strictly:\n\n"
        f"1. WARM INTRODUCTION:\n"
        f"   - Start with: \"Welcome to [topic]! In this section, you'll discover...\"\n"
        f"   - Hook the student with why this matters for their AI/ML journey\n"
        f"   - Set clear expectations: \"By the end, you'll be able to...\"\n\n"
        f"2. THEORY - EXPLAINED LIKE A FRIEND:\n"
        f"   - Define concepts using simple language first, then technical terms\n"
        f"   - Use analogies: \"Think of variables like labeled boxes...\"\n"
        f"   - Explain the \"why\" before the \"how\"\n"
        f"   - Include \"💡 Pro Tip\", \"⚠️ Common Mistake\", \"🤔 Think About It\" callouts\n"
        f"   - Build intuition before diving into details\n"
        f"   - Connect to ML/AI context: \"You'll use this when...\"\n\n"
        f"3. CODE EXAMPLES - LEARN BY DOING:\n"
        f"   - 4-6 examples per topic, starting with \"Hello World\" simplicity\n"
        f"   - Introduce each example: \"Let's see this in action...\"\n"
        f"   - Walk through code line-by-line as if explaining to a friend\n"
        f"   - Show expected output and explain what happened\n"
        f"   - Include variations: \"What if we change this?\"\n"
        f"   - Relate examples to data science tasks\n\n"
        f"4. YOUR TURN - PRACTICE EXERCISES:\n"
        f"   - 5-7 exercises with encouraging prompts\n"
        f"   - Start with: \"Now it's your turn to try...\"\n"
        f"   - Provide helpful starter code with \"# TODO\" comments\n"
        f"   - Give step-by-step solution outlines, not just answers\n"
        f"   - Include hints: \"Stuck? Try thinking about...\"\n\n"
        f"5. LEARNING AIDS:\n"
        f"   - \"Key Takeaways\" summary: \"Remember these important points...\"\n"
        f"   - \"What's Next\" preview: \"In the next section, we'll build on this...\"\n"
        f"   - Recommended resources with context: \"If you want to dive deeper...\"\n\n"
        f"Create welcoming overview, learning objectives, prerequisites, key terms, estimated duration.\n"
        f"Context: {guidance}\n\n"
        f"Return minimal overview - detailed content is already in submodules."
    )
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        functions=module_function,
        function_call={"name": "build_module"},
        temperature=0.4,
    )
    msg = completion.choices[0].message
    
    if getattr(msg, "function_call", None) and getattr(msg.function_call, "arguments", None):
        try:
            args = json.loads(msg.function_call.arguments)
        except Exception:
            args = {"name": module_name, "overview": "", "learning_objectives": [], "prerequisites": [], "estimated_duration": "", "key_terms": [], "topics": [], "detailed_content": [], "exercises": [], "resources": []}
        if "name" not in args:
            args["name"] = module_name
        args["hierarchical_structure"] = structure
        return args
    return {"name": module_name, "overview": "", "learning_objectives": [], "prerequisites": [], "estimated_duration": "", "key_terms": [], "topics": [], "detailed_content": [], "exercises": [], "resources": [], "hierarchical_structure": structure}

def build_course():
    course = {
        "title": "Python & Data for AI - Your First Steps into Machine Learning",
        "audience": "You - a complete beginner excited to learn Python for AI and Data Science!",
        "level": "Beginner → Intermediate (We'll take it step by step)",
        "outcome": "By the end of this course, you'll confidently use Python to analyze data, create visualizations, and prepare datasets for machine learning - no prior coding experience needed!",
        "modules": [],
    }
    specs = [
        {
            "name": "Python Basics",
            "guidance": "Installation and running code, REPL vs scripts, syntax and indentation, numbers and arithmetic, strings and f-strings, booleans, lists, tuples, dicts, sets, operators, conditionals, input/output, simple exceptions. Include examples mirroring data tasks such as parsing lines, counting frequencies, and simple data transforms.",
        },
        {
            "name": "Variables, Loops, Functions",
            "guidance": "Variable naming and scope, mutability vs immutability, for/while loops, break/continue, enumerate and zip, list/dict/set comprehensions, function definitions with type hints and docstrings, default args, *args/**kwargs, pure vs impure functions, recursion vs iteration at a basic level. Include patterns frequently used in data processing.",
        },
        {
            "name": "Working with Data (CSV, JSON)",
            "guidance": "File I/O with context managers, csv.reader/DictReader and writer/DictWriter, quoting and dialects, reading and writing JSON with json.loads/dumps, basic validation and error handling, summarizing tabular data (min, max, mean), merging small JSON structures. Include a small realistic CSV and JSON example pipeline.",
        },
        {
            "name": "Numpy, Pandas",
            "guidance": "NumPy arrays, dtype and shape, slicing and boolean indexing, broadcasting and vectorization, aggregation; Pandas Series/DataFrame, read_csv, dtypes, selecting rows/cols with loc/iloc, filtering, groupby-agg, joins/merges, handling missing values, apply vs vectorized ops, exporting to CSV. Emphasize tasks common in ML data prep.",
        },
        {
            "name": "Plotting with Matplotlib",
            "guidance": "Matplotlib basics, line, bar, scatter, histogram, box plot, styling and annotations, subplots and figure layout, saving figures, integrating with Pandas for quick plots. Include examples that visualize distributions and relationships relevant to ML datasets.",
        },
        {
            "name": "Mini-Project: Student Marks Analyzer",
            "guidance": "End-to-end project: read a marks CSV, compute per-student and per-subject statistics, handle missing values, derive grades, identify top/bottom performers, visualize distributions and trends with Matplotlib, export a summary report as CSV/JSON. Provide a project section with problem_statement, dataset description, milestones, rubric, and extensions.",
        },
    ]
    modules = []
    total = len(specs)
    for idx, spec in enumerate(specs, 1):
        module = generate_module(spec["name"], spec["guidance"], idx, total)
        modules.append(module)
    course["modules"] = modules
    return course

def format_course_as_text(course):
    """Convert course JSON to beautifully formatted text."""
    lines = []
    
    lines.append("=" * 100)
    lines.append(course["title"].center(100))
    lines.append("=" * 100)
    lines.append("")
    lines.append("🎓 Welcome to Your Learning Journey!")
    lines.append("")
    lines.append(f"👋 Who is this for? {course['audience']}")
    lines.append(f"📈 Your Path: {course['level']}")
    lines.append(f"🎯 What You'll Achieve: {course['outcome']}")
    lines.append("")
    lines.append("💪 Ready to start? Let's dive in! Remember: everyone starts as a beginner.")
    lines.append("    Take your time, practice the examples, and don't hesitate to revisit sections.")
    lines.append("")
    lines.append("=" * 100)
    lines.append("")
    
    for module_idx, module in enumerate(course.get("modules", []), 1):
        lines.append("\n" + "#" * 100)
        lines.append(f"MODULE {module_idx}: {module.get('name', 'Untitled')}")
        lines.append("#" * 100)
        lines.append("")
        
        if module.get("overview"):
            lines.append("📝 OVERVIEW")
            lines.append("-" * 100)
            lines.append(module["overview"])
            lines.append("")
        
        # Display hierarchical structure navigation
        hierarchical = module.get("hierarchical_structure", {})
        if hierarchical.get("submodules"):
            lines.append("📋 MODULE STRUCTURE")
            lines.append("-" * 100)
            for sm_idx, submodule in enumerate(hierarchical["submodules"], 1):
                lines.append(f"  {sm_idx}. {submodule.get('name', '')}")
                for ssm_idx, sub_sub in enumerate(submodule.get("sub_submodules", []), 1):
                    lines.append(f"     {sm_idx}.{ssm_idx} {sub_sub.get('name', '')}")
            lines.append("")
        
        if module.get("estimated_duration"):
            lines.append(f"⏱️  Estimated Duration: {module['estimated_duration']}")
            lines.append("")
        
        if module.get("prerequisites"):
            lines.append("📋 PREREQUISITES")
            lines.append("-" * 100)
            for prereq in module["prerequisites"]:
                lines.append(f"  • {prereq}")
            lines.append("")
        
        if module.get("learning_objectives"):
            lines.append("🎯 LEARNING OBJECTIVES")
            lines.append("-" * 100)
            for obj in module["learning_objectives"]:
                lines.append(f"  ✓ {obj}")
            lines.append("")
        
        if module.get("key_terms"):
            lines.append("🔑 KEY TERMS")
            lines.append("-" * 100)
            lines.append("  " + ", ".join(module["key_terms"]))
            lines.append("")
        
        # Display hierarchical content
        hierarchical = module.get("hierarchical_structure", {})
        if hierarchical.get("submodules"):
            lines.append("\n" + "=" * 100)
            lines.append("📚 DETAILED CONTENT (HIERARCHICAL)")
            lines.append("=" * 100)
            lines.append("")
            
            for sm_idx, submodule in enumerate(hierarchical["submodules"], 1):
                lines.append(f"\n{'━' * 100}")
                lines.append(f"📖 SUBMODULE {sm_idx}: {submodule.get('name', 'Untitled')}")
                lines.append("━" * 100)
                if submodule.get("description"):
                    lines.append(f"Description: {submodule['description']}")
                lines.append("")
                
                for ssm_idx, sub_sub in enumerate(submodule.get("sub_submodules", []), 1):
                    content = sub_sub.get("content", {})
                    lines.append(f"\n  {'─' * 95}")
                    lines.append(f"  📘 {sm_idx}.{ssm_idx} {sub_sub.get('name', 'Untitled')}")
                    lines.append(f"  {'─' * 95}")
                    if sub_sub.get("description"):
                        lines.append(f"  {sub_sub['description']}")
                    lines.append("")
                    
                    # Theory
                    if content.get("theory"):
                        lines.append("  📚 Theory:")
                        lines.append("  " + "·" * 95)
                        theory_lines = content["theory"].split("\n")
                        for tline in theory_lines:
                            lines.append(f"  {tline}")
                        lines.append("")
                    
                    # Key Points
                    if content.get("key_points"):
                        lines.append("  🔑 Key Points:")
                        for point in content["key_points"]:
                            lines.append(f"    • {point}")
                        lines.append("")
                    
                    # Code Examples
                    if content.get("code_examples"):
                        lines.append("  💻 Code Examples:")
                        for ex_idx, example in enumerate(content["code_examples"], 1):
                            lines.append(f"\n    Example {ex_idx}: {example.get('title', 'Code')}")
                            if example.get("explanation"):
                                lines.append(f"    {example['explanation']}")
                            if example.get("code"):
                                lines.append("    ```python")
                                for code_line in example["code"].split("\n"):
                                    lines.append(f"    {code_line}")
                                lines.append("    ```")
                            if example.get("output"):
                                lines.append("    Output:")
                                lines.append("    ```")
                                for out_line in example["output"].split("\n"):
                                    lines.append(f"    {out_line}")
                                lines.append("    ```")
                            lines.append("")
                    
                    # Exercises
                    if content.get("exercises"):
                        lines.append("  ✏️  Practice Exercises:")
                        for ex_idx, exercise in enumerate(content["exercises"], 1):
                            lines.append(f"\n    Exercise {ex_idx}:")
                            if exercise.get("task"):
                                lines.append(f"    Task: {exercise['task']}")
                            if exercise.get("starter_code"):
                                lines.append("    Starter Code:")
                                lines.append("    ```python")
                                for code_line in exercise["starter_code"].split("\n"):
                                    lines.append(f"    {code_line}")
                                lines.append("    ```")
                            if exercise.get("hints"):
                                lines.append("    💡 Hints:")
                                for hint in exercise["hints"]:
                                    lines.append(f"      • {hint}")
                            lines.append("")
        
        # Fallback to old format if no hierarchical structure
        elif module.get("detailed_content"):
            lines.append("\n" + "=" * 100)
            lines.append("📚 DETAILED CONTENT")
            lines.append("=" * 100)
            lines.append("")
            
            for content_idx, content in enumerate(module["detailed_content"], 1):
                lines.append(f"\n{'─' * 100}")
                lines.append(f"Section {content_idx}: {content.get('title', 'Untitled')}")
                lines.append("─" * 100)
                lines.append("")
                
                if content.get("explanation"):
                    lines.append(content["explanation"])
                    lines.append("")
                
                if content.get("code_examples"):
                    for ex_idx, example in enumerate(content["code_examples"], 1):
                        lines.append(f"\n💻 Example {ex_idx}: {example.get('title', 'Code Example')}")
                        lines.append("~" * 100)
                        
                        if example.get("explanation"):
                            lines.append(example["explanation"])
                            lines.append("")
                        
                        if example.get("code"):
                            lines.append("Code:")
                            lines.append("```python")
                            lines.append(example["code"])
                            lines.append("```")
                            lines.append("")
                        
                        if example.get("expected_output"):
                            lines.append("Expected Output:")
                            lines.append("```")
                            lines.append(example["expected_output"])
                            lines.append("```")
                            lines.append("")
        
        if module.get("exercises"):
            lines.append("\n" + "=" * 100)
            lines.append("✏️  PRACTICE EXERCISES")
            lines.append("=" * 100)
            lines.append("")
            
            for ex_idx, exercise in enumerate(module["exercises"], 1):
                lines.append(f"\nExercise {ex_idx}:")
                lines.append("-" * 100)
                
                if exercise.get("prompt"):
                    lines.append(f"📝 Task: {exercise['prompt']}")
                    lines.append("")
                
                if exercise.get("starter_code"):
                    lines.append("Starter Code:")
                    lines.append("```python")
                    lines.append(exercise["starter_code"])
                    lines.append("```")
                    lines.append("")
                
                if exercise.get("solution_outline"):
                    lines.append("💡 Solution Outline:")
                    lines.append(exercise["solution_outline"])
                    lines.append("")
        
        
        if module.get("project"):
            project = module["project"]
            lines.append("\n" + "=" * 100)
            lines.append("🚀 MINI-PROJECT")
            lines.append("=" * 100)
            lines.append("")
            
            if project.get("title"):
                lines.append(f"Project Title: {project['title']}")
                lines.append("")
            
            if project.get("problem_statement"):
                lines.append("Problem Statement:")
                lines.append("-" * 100)
                lines.append(project["problem_statement"])
                lines.append("")
            
            if project.get("dataset"):
                lines.append("Dataset Description:")
                lines.append("-" * 100)
                lines.append(project["dataset"])
                lines.append("")
            
            if project.get("milestones"):
                lines.append("Project Milestones:")
                lines.append("-" * 100)
                for m_idx, milestone in enumerate(project["milestones"], 1):
                    lines.append(f"  {m_idx}. {milestone}")
                lines.append("")
            
            if project.get("rubric"):
                lines.append("Grading Rubric:")
                lines.append("-" * 100)
                for rubric_item in project["rubric"]:
                    lines.append(f"  • {rubric_item}")
                lines.append("")
            
            if project.get("extensions"):
                lines.append("Extension Ideas:")
                lines.append("-" * 100)
                for ext in project["extensions"]:
                    lines.append(f"  + {ext}")
                lines.append("")
        
        if module.get("resources"):
            lines.append("\n" + "=" * 100)
            lines.append("📚 ADDITIONAL RESOURCES")
            lines.append("=" * 100)
            lines.append("")
            for resource in module["resources"]:
                lines.append(f"  • {resource}")
            lines.append("")
    
    quiz_data = course.get("comprehensive_quiz", {})
    if quiz_data.get("questions"):
        lines.append("\n\n" + "#" * 100)
        lines.append("🎓 FINAL QUIZ - TEST YOUR KNOWLEDGE!")
        lines.append("#" * 100)
        lines.append("")
        lines.append("🎉 Congratulations on completing all the modules!")
        lines.append("")
        
        if quiz_data.get("instructions"):
            lines.append("📋 How This Quiz Works:")
            lines.append("-" * 100)
            lines.append(quiz_data["instructions"])
            lines.append("")
        
        lines.append("\n💡 This quiz helps you review everything you've learned.")
        lines.append("   Don't worry about getting everything right - this is about learning!")
        lines.append(f"\n📊 Total Questions: {len(quiz_data.get('questions', []))}")
        lines.append("   Mix of beginner 🟢, intermediate 🟡, and medium 🟠 difficulty")
        lines.append("")
        lines.append("✨ Take your time and think through each question. Good luck!")
        lines.append("")
        
        for q_idx, question in enumerate(quiz_data["questions"], 1):
            lines.append("\n" + "=" * 100)
            lines.append(f"Question {q_idx}")
            if question.get("module"):
                lines.append(f"Module: {question['module']}")
            if question.get("difficulty"):
                difficulty_emoji = {"beginner": "🟢", "intermediate": "🟡", "medium": "🟠"}
                emoji = difficulty_emoji.get(question['difficulty'], "")
                lines.append(f"Difficulty: {emoji} {question['difficulty'].title()}")
            lines.append("=" * 100)
            lines.append("")
            lines.append(question.get("question", ""))
            lines.append("")
            
            if question.get("options"):
                for opt_idx, option in enumerate(question["options"]):
                    letter = chr(65 + opt_idx)
                    lines.append(f"  {letter}) {option}")
                lines.append("")
            
            answer_idx = question.get("answer_index")
            if answer_idx is not None:
                answer_letter = chr(65 + answer_idx)
                lines.append(f"✅ Correct Answer: {answer_letter}")
            
            if question.get("explanation"):
                lines.append(f"\n💡 Explanation:")
                lines.append(question["explanation"])
            lines.append("")
    
    lines.append("\n" + "=" * 100)
    lines.append("🎊 CONGRATULATIONS - YOU'VE COMPLETED THE COURSE! 🎊")
    lines.append("=" * 100)
    lines.append("")
    lines.append("🌟 Amazing work! You've taken your first steps into the world of Python, Data, and AI.")
    lines.append("")
    lines.append("📚 What You've Accomplished:")
    lines.append("   ✓ Mastered Python fundamentals")
    lines.append("   ✓ Learned to work with real data (CSV, JSON)")
    lines.append("   ✓ Explored NumPy and Pandas for data analysis")
    lines.append("   ✓ Created visualizations with Matplotlib")
    lines.append("   ✓ Built a complete data analysis project")
    lines.append("")
    lines.append("🚀 Next Steps on Your Journey:")
    lines.append("   • Practice, practice, practice - build your own projects!")
    lines.append("   • Explore machine learning libraries like scikit-learn")
    lines.append("   • Join data science communities and keep learning")
    lines.append("   • Remember: every expert was once a beginner")
    lines.append("")
    lines.append("💙 Keep coding, keep learning, and enjoy the journey!")
    lines.append("=" * 100)
    
    return "\n".join(lines)

def generate_comprehensive_quiz(course):
    content_summary = []
    for module in course.get("modules", []):
        module_info = {
            "name": module.get("name", ""),
            "key_terms": module.get("key_terms", []),
            "learning_objectives": module.get("learning_objectives", []),
            "topics": []
        }
        for content in module.get("detailed_content", []):
            module_info["topics"].append(content.get("title", ""))
        content_summary.append(module_info)
    
    system_prompt = "You are a supportive teacher creating a quiz for students who just completed their first Python for AI course. Write questions that help students TEST their understanding while also REINFORCING learning. Be encouraging and educational."
    user_prompt = (
        f"Based on the following course modules, create a friendly, comprehensive quiz:\n\n"
        f"Course Content Summary:\n{json.dumps(content_summary, indent=2)}\n\n"
        f"Generate 12-15 multiple-choice questions with these characteristics:\n\n"
        f"STYLE & TONE:\n"
        f"- Write questions as if asking a student: \"Which approach would you use to...\"\n"
        f"- Make scenarios realistic: \"You're analyzing customer data and need to...\"\n"
        f"- Avoid trick questions - test real understanding\n"
        f"- Be clear and unambiguous\n\n"
        f"CONTENT COVERAGE:\n"
        f"- Cover all 6 modules proportionally\n"
        f"- Mix theoretical (\"What is...\") and practical (\"How would you...\")\n"
        f"- Include beginner (🟢), intermediate (🟡), and medium (🟠) difficulty\n"
        f"- Focus on ML/AI-relevant Python concepts\n\n"
        f"ANSWER OPTIONS:\n"
        f"- Provide 4 plausible options (avoid obviously wrong answers)\n"
        f"- Make distractors educational (common misconceptions)\n\n"
        f"EXPLANATIONS:\n"
        f"- Explain WHY the correct answer is right\n"
        f"- Briefly mention why other options are incorrect\n"
        f"- Reinforce the learning point\n"
        f"- Use encouraging language: \"Great! The correct answer is...\"\n\n"
        f"Return as a JSON object with this structure:\n"
        f"{{\n"
        f"  \"instructions\": \"Friendly instructions: 'Congratulations on completing the course! This quiz will help you...'\",\n"
        f"  \"questions\": [\n"
        f"    {{\n"
        f"      \"module\": \"Module name\",\n"
        f"      \"difficulty\": \"beginner|intermediate|medium\",\n"
        f"      \"question\": \"Question in conversational, student-friendly tone\",\n"
        f"      \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
        f"      \"answer_index\": 0,\n"
        f"      \"explanation\": \"Encouraging explanation that reinforces learning\"\n"
        f"    }}\n"
        f"  ]\n"
        f"}}"
    )
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.5,
    )
    
    try:
        quiz_data = json.loads(completion.choices[0].message.content)
        print(f"✅ Quiz: {len(quiz_data.get('questions', []))} questions")
        return quiz_data
    except Exception as e:
        print(f"⚠️ Quiz generation failed: {e}")
        return {"instructions": "Complete the following quiz questions.", "questions": []}

def generate_pdf_book(course, quiz):
    print("📝 Generating PDF...")
    pdf_filename = "python_data_for_ai_book.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    Story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495E'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=10
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    )
    
    code_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        leftIndent=20,
        rightIndent=20,
        spaceAfter=10,
        spaceBefore=10,
        backColor=colors.HexColor('#F5F5F5'),
        borderColor=colors.HexColor('#CCCCCC'),
        borderWidth=1,
        borderPadding=10
    )
    
    # Title Page
    from reportlab.platypus import HRFlowable
    Story.append(Spacer(1, 1.5*inch))
    Story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor('#3498db'), spaceAfter=20))
    
    Story.append(Paragraph(course.get('title', 'Python & Data for AI'), title_style))
    Story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor('#3498db'), spaceBefore=10, spaceAfter=30))
    
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=12, textColor=colors.HexColor('#7F8C8D'), alignment=TA_CENTER, spaceAfter=20)
    Story.append(Paragraph("A Comprehensive Beginner's Guide", subtitle_style))
    Story.append(Spacer(1, 0.3*inch))
    Story.append(Paragraph(course.get('audience', ''), subtitle_style))
    Story.append(Spacer(1, 1*inch))
    
    from datetime import datetime
    info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, alignment=TA_CENTER, textColor=colors.grey)
    Story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", info_style))
    
    Story.append(PageBreak())
    
    for module_idx, module in enumerate(course.get('modules', []), 1):
        # Module title
        Story.append(Paragraph(f"Chapter {module_idx}: {module.get('name', '')}", heading_style))
        Story.append(Spacer(1, 0.2*inch))
        
        if module.get('overview'):
            Story.append(Paragraph(module['overview'], body_style))
            Story.append(Spacer(1, 0.2*inch))
        
        # Hierarchical content
        hierarchical = module.get('hierarchical_structure', {})
        if hierarchical.get('submodules'):
            for sm_idx, submodule in enumerate(hierarchical['submodules'], 1):
                # Submodule
                Story.append(Paragraph(f"{module_idx}.{sm_idx} {submodule.get('name', '')}", subheading_style))
                
                for ssm_idx, sub_sub in enumerate(submodule.get('sub_submodules', []), 1):
                    content = sub_sub.get('content', {})
                    
                    # Sub-submodule title
                    Story.append(Paragraph(f"{module_idx}.{sm_idx}.{ssm_idx} {sub_sub.get('name', '')}", 
                                         styles['Heading4']))
                    Story.append(Spacer(1, 0.1*inch))
                    
                    # Theory
                    if content.get('theory'):
                        Story.append(Paragraph(content['theory'], body_style))
                        Story.append(Spacer(1, 0.1*inch))
                    
                    # Table if available - Beautiful styling with KeepTogether
                    if content.get('table_data') and content['table_data'].get('rows'):
                        table_data = content['table_data']
                        if table_data.get('headers'):
                            table_elements = []
                            table_elements.append(Spacer(1, 0.15*inch))
                            
                            # Table title
                            if table_data.get('caption'):
                                table_title_style = ParagraphStyle('TableTitle', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold', textColor=colors.HexColor('#34495e'), spaceAfter=6)
                                table_elements.append(Paragraph(f"📊 {table_data['caption']}", table_title_style))
                            
                            table_content = [table_data['headers']] + table_data.get('rows', [])
                            t = Table(table_content, hAlign='LEFT')
                            t.setStyle(TableStyle([
                                # Header row
                                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('FONTSIZE', (0, 0), (-1, 0), 10),
                                ('TOPPADDING', (0, 0), (-1, 0), 12),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                # Data rows
                                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                                ('FONTSIZE', (0, 1), (-1, -1), 9),
                                ('TOPPADDING', (0, 1), (-1, -1), 8),
                                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                                # Borders
                                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDC3C7')),
                                ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#3498db')),
                                # Alternating row colors
                                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
                            ]))
                            table_elements.append(t)
                            table_elements.append(Spacer(1, 0.15*inch))
                            
                            # Wrap table in KeepTogether to prevent page breaks inside table
                            Story.append(KeepTogether(table_elements))
                    
                    # Code examples - wrapped in KeepTogether
                    if content.get('code_examples'):
                        for example in content['code_examples']:
                            code_elements = []
                            code_elements.append(Spacer(1, 0.15*inch))
                            
                            # Example title with icon
                            example_title_style = ParagraphStyle('ExampleTitle', parent=styles['Normal'], fontSize=11, textColor=colors.HexColor('#2980b9'), fontName='Helvetica-Bold', spaceAfter=8)
                            code_elements.append(Paragraph(f"💻 {example.get('title', 'Example')}", example_title_style))
                            
                            if example.get('code'):
                                code_lines = example['code'].split('\n')
                                formatted_lines = []
                                for line in code_lines:
                                    leading_spaces = len(line) - len(line.lstrip())
                                    indent = '&nbsp;' * (leading_spaces * 2)
                                    cleaned = line.strip().replace('<', '&lt;').replace('>', '&gt;')
                                    formatted_lines.append(indent + cleaned)
                                code_clean = '<br/>'.join(formatted_lines)
                                code_para = Paragraph(f'<font name="Courier" size="9" color="#2C3E50">{code_clean}</font>', styles['Code'])
                                
                                # Wrap in table for background color
                                code_table = Table([[code_para]], colWidths=[5.5*inch])
                                code_table.setStyle(TableStyle([
                                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8F9FA')),
                                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#DEE2E6')),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 12),
                                    ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                                ]))
                                code_elements.append(code_table)
                                code_elements.append(Spacer(1, 0.08*inch))
                            
                            if example.get('explanation'):
                                code_elements.append(Paragraph(example['explanation'], body_style))
                            
                            # Keep code block together on same page
                            Story.append(KeepTogether(code_elements))
                    
                    # Key points - styled box wrapped in KeepTogether
                    if content.get('key_points'):
                        key_elements = []
                        key_elements.append(Spacer(1, 0.15*inch))
                        
                        # Create key points box
                        key_points_content = []
                        key_title_style = ParagraphStyle('KeyTitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#27ae60'), spaceAfter=8)
                        key_points_content.append(Paragraph("🔑 Key Takeaways", key_title_style))
                        
                        bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=10, leftIndent=10, spaceAfter=6)
                        for point in content['key_points']:
                            key_points_content.append(Paragraph(f"✓ {point}", bullet_style))
                        
                        # Combine all points
                        combined_points = []
                        for p in key_points_content:
                            combined_points.append([p])
                        
                        key_table = Table(combined_points, colWidths=[5.5*inch])
                        key_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F8F5')),
                            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#27ae60')),
                            ('LEFTPADDING', (0, 0), (-1, -1), 15),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
                            ('TOPPADDING', (0, 0), (-1, -1), 10),
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                        ]))
                        key_elements.append(key_table)
                        
                        # Keep key takeaways together on same page
                        Story.append(KeepTogether(key_elements))
                    
                    Story.append(Spacer(1, 0.25*inch))
        
        Story.append(PageBreak())
    
    # Add quiz section
    if quiz and quiz.get('questions'):
        Story.append(Paragraph("📝 Comprehensive Quiz", heading_style))
        Story.append(Spacer(1, 0.2*inch))
        
        if quiz.get('instructions'):
            Story.append(Paragraph(quiz['instructions'], body_style))
            Story.append(Spacer(1, 0.3*inch))
        
        quiz_question_style = ParagraphStyle(
            'QuizQuestion',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        quiz_option_style = ParagraphStyle(
            'QuizOption',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=5
        )
        
        for idx, question in enumerate(quiz['questions'], 1):
            Story.append(Paragraph(f"Q{idx}. {question.get('question', '')}", quiz_question_style))
            
            for opt_idx, option in enumerate(question.get('options', []), 1):
                opt_letter = chr(64 + opt_idx)
                Story.append(Paragraph(f"{opt_letter}. {option}", quiz_option_style))
            
            if question.get('explanation'):
                explanation_style = ParagraphStyle(
                    'Explanation',
                    parent=styles['Normal'],
                    fontSize=9,
                    textColor=colors.HexColor('#7F8C8D'),
                    leftIndent=20,
                    spaceAfter=10,
                    spaceBefore=5
                )
                correct_answer = chr(65 + question.get('answer_index', 0))
                Story.append(Paragraph(f"✓ Answer: {correct_answer} - {question['explanation']}", explanation_style))
            
            Story.append(Spacer(1, 0.15*inch))
    
    doc.build(Story)
    return pdf_filename

def main():
    print("\n" + "=" * 100)
    print("PYTHON & DATA FOR AI - PDF BOOK GENERATOR".center(100))
    print("=" * 100)
    
    course = build_course()
    
    print("\n📝 Generating quiz...")
    quiz = generate_comprehensive_quiz(course)
    course["comprehensive_quiz"] = quiz
    
    print("\n📄 Saving text files...")
    text_content = format_course_as_text(course)
    
    out_file_txt = "python_data_for_ai_curriculum.txt"
    out_file_json = "python_data_for_ai_curriculum.json"
    
    with open(out_file_txt, "w", encoding="utf-8") as f:
        f.write(text_content)
    
    with open(out_file_json, "w", encoding="utf-8") as f:
        json.dump(course, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Text files saved: {out_file_txt}, {out_file_json}")
    print(f"\n📄 Creating PDF book...")
    pdf_file = generate_pdf_book(course, quiz)
    
    print(f"\n✅ PDF generated: {pdf_file}")
    print(f"📊 Quiz questions: {len(quiz.get('questions', []))}")
    print(f"🎉 Complete! (~30-40 pages)\n")

if __name__ == "__main__":
    main()

