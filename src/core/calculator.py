class GammaCalculator:
    @staticmethod
    def calculate_gamma(original_red, original_green, original_blue, temperature):
        """calculate gamma values for a given temperature"""
        r_factor = 1.0
        g_factor = 0.5 + (0.5 * temperature)
        b_factor = temperature
        new_r = [int(val * r_factor) for val in original_red]
        new_g = [int(val * g_factor) for val in original_green]
        new_b = [int(val * b_factor) for val in original_blue]
        return {"r": new_r, "g": new_g, "b": new_b}
