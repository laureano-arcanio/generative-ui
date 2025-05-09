import random
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from app.types.generative import GenerativeCreate, GenerativeDetail

from app.config import settings

class GenerativeService:
    """
    """

    model = init_chat_model("gpt-4.1-nano", model_provider="openai", api_key=settings.get_openai_api_key())

    def __init__(self):
        self.target_audiences = [
            {
                "id": 1,
                "prompt": "Event organizers looking to create a user-friendly form for event registration.",
                "persona": "Event Organizer",
            },
            {
                "id": 2,
                "prompt": "Personal coaches building introspective intake forms for their clients.",
                "persona": "Personal Coach",
            },
            {
                "id": 3,
                "prompt": "HR managers creating onboarding and employee insight forms with complex level of details.",
                "persona": "HR Manager",    
            },

        ]

        self.designers = [
            {
                "id": 1,
                "prompt": """
                    I prefer a clean, modern, minimalist design with generous white space, subtle typography, and a neutral color palette (e.g., black, white, light gray).
                    Content should be direct, well-organized, and free of unnecessary visual embellishments or gradients.
                    Emphasize clarity, simplicity, and hierarchy of information through typographic scale and spacing.
                    Action buttons should be bold and high-contrast but remain minimal in styling, with flat colors and no shadows.
                    Icons are optional; if used, they should be simple, monochromatic, and line-based to maintain minimalism.
                    Avoid borders unless necessary for separation; rely on spacing and alignment to guide the user.
                """,
                "persona": "Minimalist Designer",
            },
            {
                "id": 2,
                "prompt": """
                    I want a fun, colorful, and lively UI that feels energetic and modern—targeted for young adults or creative professionals, not for children.
                    Use rounded corners, soft shadows, and vibrant accent colors to make the interface approachable and dynamic, while avoiding overly cartoonish or exaggerated elements.
                    Include tasteful illustrative icons or small decorative graphics alongside feature lists to convey friendliness without being childish.
                    Typography can be slightly expressive (e.g., a geometric or rounded sans-serif), but maintain professionalism and legibility.
                    Buttons should use bold, saturated colors with subtle hover animations (like color shifts or scale) to add personality without being playful in a juvenile sense.
                    Backgrounds may include soft gradients or subtle patterns for depth, but should avoid overly bright or primary color palettes typical of children's designs.
                """,
                "persona": "Playful & Creative Designer",
            },
            {
                "id": 3,
                "prompt": """
                    I prefer a formal, polished, enterprise-level design with structured grid layouts, sharp lines, and a professional color palette (e.g., white, dark gray, navy, with subtle accent colors like blue or green).
                    Icons should be minimal, monochromatic, and professional, aligning with modern business software aesthetics.
                    Use clear, legible typography with consistent font weights (e.g., medium for body, bold for headings) to convey trust, reliability, and authority.
                    Buttons should have clear outlines or solid fills with subtle hover states, avoiding flashy animations.
                    Layouts should prioritize information hierarchy with strong alignment and spacing, using dividers or subtle background shades for section separation.
                    Avoid decorative elements that don’t serve a functional or communicative purpose.
                """,
                "persona": "Professional & Corporate Designer",
            }
        ]
    
    def get_system_message(self, tech_requirements=None, ui_requirements=None, target_audience=None, design_guidelines=None):
        """
        Generate a system message with dynamic values for different sections.
        
        Parameters:
        - tech_requirements: Technical requirements to include
        - ui_requirements: UI Component requirements to include
        - target_audience: Target audience description to include
        - design_guidelines: Design guidelines to include
        
        Returns:
        - Formatted system message string
        """
        # Create variations of technical requirements
        tech_variations = [
            """Use React and inline CSS for styling.
            Use functional components and hooks.
            Focus on responsive design principles.
            Ensure compatibility with modern browsers and accessibility standards.""",
            
            """Use React with Material UI components.
            Apply modern hooks pattern for state management.
            Ensure components are accessible and follow WCAG guidelines.
            Optimize for performance and reusability.""",
            
            """Use React functional components.
            Implement clean separation of markup and logic.
            Use CSS-in-JS for styling with MUI.
            Ensure modularity and scalability of components."""
        ]
            
        # Create variations of UI requirements
        ui_variations = [
            """Create a form to get to know the user.
            The form should always include the following fields:
            - Full Name (text input)
            - Email Address (email input)
            - Phone Number (tel input)
            Add 3-5 additional fields based on the user target.
            Include tooltips or helper text for better user guidance.""",
            
            """Design a user profile form that captures essential information.
            Required fields include:
            - Name (text input)
            - Contact email (email input)
            - Mobile number (tel input)
            Include validation, helpful error messages, and a progress indicator for multi-step forms.""",
            
            """Build an information collection form with:
            - User's full name (text input)
            - Email for communications (email input)
            - Contact number (tel input)
            Add dynamic fields based on user preferences.
            Ensure a clear submission flow with a confirmation message."""
        ]
            
        # Create variations for design guidelines
        design_variations = [
            """Use a cohesive color scheme with at least 3 coordinating colors.
            Buttons should have distinct hover states with animations.
            Maintain consistent spacing between elements.
            Use subtle gradients or shadows to add depth to the design.""",
            
            """Apply visual hierarchy through size, color, and spacing.
            Form fields should include clear labels, helper text, and icons where appropriate.
            Use smooth transitions and animations for interactive elements.
            Keep the interface clean, focused, and visually appealing.""",
            
            """Implement thoughtful spacing for improved readability.
            Use colors strategically to guide attention and create contrast.
            Make sure error states are clearly visible with detailed messages.
            Form layout should guide the user through completion steps with visual cues."""
        ]
        
        default_target_audience = """some target audience examples:
            - Event organizers looking to create a user-friendly form for event registration.
            - Personal coaches building introspective intake forms for their clients."""
            
        # Choose random variations if no specific requirements are provided
        tech_requirements = tech_requirements or random.choice(tech_variations)
        ui_requirements = ui_requirements or random.choice(ui_variations)
        target_audience = target_audience or default_target_audience
        
        # Only randomize design guidelines if not explicitly provided from a designer
        if design_guidelines is None or design_guidelines == "":
            design_guidelines = random.choice(design_variations)
        
        # Add randomization instructions to encourage variety
        randomization_prompt = f"""
            Make this implementation unique by:
            - Using a {random.choice(['minimalist', 'playful', 'professional', 'modern', 'artistic'])} approach
            - Focusing on {random.choice(['usability', 'visual appeal', 'efficiency', 'clarity', 'engagement'])}
            - Including {random.choice(['subtle animations', 'thoughtful microcopy', 'intuitive validation', 'visual feedback', 'progressive disclosure'])}
            - Each time you generate, create a different layout and component arrangement
            - Incorporate advanced design elements like {random.choice(['gradient backgrounds', 'micro-interactions', 'custom icons', 'dynamic field validation', 'multi-step progress indicators'])}
        """
        
        return f"""
            You are a React component generator. You will receive a user preference and generate a React component based on it.
            Follow these instructions carefully:
            Make sure its a valid React component.
            Output a single, complete React component as a valid JSX expression.
            Do not include import statements, export statements, or variable declarations.
            Do not add code comments, backslashes, or line breaks (\\n).
            Do not wrap the output in markdown code blocks or syntax highlighting tags.
            Return only the JSX, written in a single line of text.
            The code must compile without errors in React and work inside react-live.
            Do not include const or function keywords—only output the JSX expression directly.
            do not write inline javascript code inside the JSX.
            Do not use any external libraries or frameworks except for MUI.
            If needed, Use MUI components, prepend MUI.ComponentName to the component name. Example: MUI.Button, MUI.TextField.
            Make sure not to repeat MUI.MUI.ComponentName. Example: MUI.MUI.Button, MUI.MUI.TextField.
            If needed, use MUI icons, choose only from this list with exact same module prefix: ICONS.Home, ICONS.Add, ICONS.Delete, ICONS.Search, ICONS.Menu, ICONS.Settings, ICONS.Person, ICONS.Star, ICONS.Edit, ICONS.ArrowBack
            Do not use styled components
            Return only the JSX, written in a single line of text.
            Do not include any other text or explanation.
            Do not include any other function outside the component.

            Technical requirements:
            {tech_requirements}

            UI Component requirements:
            {ui_requirements}
            - Add 4-10 additional fields based on the user target.

            Target audience:
            {target_audience}

            Design guidelines:
            use the following design guidelines as a base:
            {design_guidelines}
            
            {randomization_prompt}
        """
    
    async def build_generative_component(self, generative_schema: GenerativeCreate ) -> GenerativeDetail:
        """
        """


        # self.model = OllamaLLM(model="llama3.2:3b", base_url="ollama:11434")

        persona_id = generative_schema.persona_id
        designer_id = generative_schema.designer_id if hasattr(generative_schema, 'designer_id') else persona_id
        
        # Get the appropriate persona prompt and designer prompt
        persona_index = persona_id - 1 if persona_id <= len(self.target_audiences) else 0
        designer_index = designer_id - 1 if designer_id <= len(self.designers) else 0
        
        user_prompt = self.designers[designer_index]["prompt"]
        
        # Get target audience from the selected persona
        target_audience = self.target_audiences[persona_index]["prompt"] if persona_id <= len(self.target_audiences) else None
        
        # Generate dynamic system message
        system_message = self.get_system_message(
            target_audience=f"The target audience is: {target_audience}" if target_audience else None,
            design_guidelines=user_prompt,
        )
        
        messages = [
            SystemMessage(system_message),
            HumanMessage(user_prompt),
        ]

        ai_message = self.model.invoke(messages).content
        # ai_message = model.invoke(messages)
        cleaned_response = ai_message.replace("\\'", "'").replace('\\"', '"')
        return GenerativeDetail(
            user_prefferences=generative_schema.user_prefferences,
            raw_component=cleaned_response,
            persona_id=persona_id,
            designer_id=designer_id,
            generated_prompt=system_message  # Include the generated prompt
        )