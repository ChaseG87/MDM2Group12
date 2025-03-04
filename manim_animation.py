from manim import *

#To run, in console write:
#
#manim -pql .\manim_animation.py BetaReduction


class BetaReductionIdentity(Scene):
    def construct(self):
        # Title
        title = Text("Identity Function", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # Calculate positions for two columns
        col_x = 0  # X position for column
        start_y = 2        # Starting Y position below title
        step_y_gap = 1.2   # Vertical gap between steps
        
        # Set up the new expression: (λx.xx(λy.xy))(λa.a)g
        lambda_expr = MathTex(
            r"(", r"\lambda x.", r"x \,", r")", r"y"
        )
        lambda_expr.move_to([col_x, start_y, 0])
        self.play(Write(lambda_expr))
        self.wait()
        
        # Step 1: First beta reduction - highlight relevant parts
        self.play(
            lambda_expr[1:3].animate.set_color(BLUE),    # λx.xx(λy.xy)
            lambda_expr[5:7].animate.set_color(RED),    # λa.a
        )
        self.wait()
        
        # Create first intermediate notation
        intermediate1 = MathTex(
            r"\lambda", r"[x := y]", r".", 
            r"x \, "
        )
        intermediate1[1].set_color(RED)  # Highlight the substitution
        intermediate1.move_to([col_x, start_y - step_y_gap, 0])
        
        # Beta reduction text 1
        beta1_text = Text("β₁-reduction", font_size=20)
        beta1_text.next_to(lambda_expr, DOWN, buff=0.1)
        
        # Transform to first intermediate
        self.play(
            Write(beta1_text),
            TransformMatchingTex(
                lambda_expr.copy(),  # Use copy to keep original visible
                intermediate1,
                transform_mismatches=True,
                fade_transform_mismatches=True
            )
        )
        self.wait()
        
        # First step result
        step1 = MathTex(
            r"y"
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