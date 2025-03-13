from manim import *

class Successor(Scene):
    def construct(self):
        # First Set of Steps
        title = Text("Successor Function", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        

        self.first_reduction()
        
        # Clear the screen
        self.clear()
        
        # Second Set of Steps
        self.second_reduction()

    def first_reduction(self):
      
        # Calculate positions for two columns
        col_x = 0  # X position for column
        start_y = 2        # Starting Y position below title
        step_y_gap = 1.2   # Vertical gap between steps
        
        # Set up the initial expression
        lambda_expr = MathTex(
            r"(", r"\lambda",  r"n", r"a", r"b.", r"a", r"(", r"n", r"a", r"b))", r"0"
        )
        lambda_expr.move_to([col_x, start_y, 0])
        self.play(Write(lambda_expr))
        self.wait()
        
        # Step 1: First beta reduction - highlight relevant parts
        self.play(
            lambda_expr[2].animate.set_color(BLUE),
            lambda_expr[7].animate.set_color(BLUE),
            lambda_expr[10].animate.set_color(BLUE),
        )
        self.wait()
        
        # Create first intermediate notation
        intermediate1 = MathTex(
            r"\lambda", r"[n := 0]", r"a", r"b.", r"a", r"(", r"n", r"a", r"b)" 
        )
        intermediate1[1].set_color(BLUE)  # Highlight the substitution
        intermediate1.move_to([col_x, start_y - step_y_gap, 0])
        
        # Beta reduction text 1
        beta1_text = Text("β₁-reduction", font_size=20)
        beta1_text.next_to(lambda_expr, DOWN, buff=0.1)
        
        # Transform to first intermediate
        self.play(
            Write(beta1_text),
            TransformMatchingTex(
                lambda_expr.copy(),
                intermediate1,
                transform_mismatches=True,
                fade_transform_mismatches=True
            )
        )
        self.wait()
        
        # First step result
        step1 = MathTex(
            r"\lambda", r"a", r"b.", r"a", r"(0", r"a", r"b)"
        )
        step1.move_to([col_x, start_y - 2*step_y_gap, 0])
        
        # Beta reduction arrow 1
        arrow1 = Arrow(intermediate1.get_bottom() + DOWN*0.1, step1.get_top() + UP*0.1, buff=0.1)
        
        # Transform to first step result
        self.play(
            Create(arrow1),
            Write(step1)
        )
        self.wait(3)

    def second_reduction(self):
        # Calculate positions for two columns
        col_x = 0  # X position for column
        start_y = 2        # Starting Y position below title
        step_y_gap = 1.2   # Vertical gap between steps
        
        # Set up the new expression
        lambda_expr = MathTex(
            r"\lambda",  r"a", r"b.", r"a", r"((", r"\lambda", r"s", r"z.", r"z)", r"a", r"b", r")"
        )
        lambda_expr.move_to([col_x, start_y, 0])
        self.play(Write(lambda_expr))
        self.wait()
        
        # Step 1: First beta reduction - highlight relevant parts
        self.play(
            lambda_expr[6].animate.set_color(BLUE),
            lambda_expr[9].animate.set_color(BLUE),
            lambda_expr[7].animate.set_color(RED),
            lambda_expr[10].animate.set_color(RED)
        )
        self.wait()
        
        # Create first intermediate notation
        intermediate1 = MathTex(
            r"\lambda", r"a", r"b.", r"a", r"(", r"\lambda", r"[s := a]", r"[z := b]",r".z", r")" 
        )
        intermediate1[6].set_color(BLUE),
        intermediate1[7].set_color(RED),
        intermediate1.move_to([col_x, start_y - step_y_gap, 0])
        
        # Beta reduction text 1
        beta1_text = Text("β₁-reduction", font_size=20)
        beta1_text.next_to(lambda_expr, DOWN, buff=0.1)
        
        # Transform to first intermediate
        self.play(
            Write(beta1_text),
            TransformMatchingTex(
                lambda_expr.copy(),
                intermediate1,
                transform_mismatches=True,
                fade_transform_mismatches=True
            )
        )
        self.wait()
        
        # First step result
        step1 = MathTex(
            r"\lambda", r"a", r"b.", r"a", r"(", r"b)"
        )
        step1.move_to([col_x, start_y - 2*step_y_gap, 0])
        
        # Beta reduction arrow 1
        arrow1 = Arrow(intermediate1.get_bottom() + DOWN*0.1, step1.get_top() + UP*0.1, buff=0.1)
        
        # Transform to first step result
        self.play(
            Create(arrow1),
            Write(step1)
        )
        self.wait(3)
