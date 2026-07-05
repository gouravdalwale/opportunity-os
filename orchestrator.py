from agents.profile_agent import analyze_profile
from agents.opportunity_agent import find_opportunities
from agents.roadmap_agent import generate_roadmap


class OpportunityOS:

    def __init__(self):
        self.context = {}

    def run(self, user_profile):

        # Store original profile
        self.context["user_profile"] = user_profile

        # -----------------------------
        # Agent 1
        # -----------------------------
        profile_analysis = analyze_profile(user_profile)

        self.context["profile_analysis"] = profile_analysis

        # -----------------------------
        # Agent 2
        # -----------------------------
        opportunities = find_opportunities(profile_analysis)

        self.context["opportunities"] = opportunities

        # -----------------------------
        # Agent 3
        # -----------------------------
        roadmap = generate_roadmap(
            profile_analysis + "\n\n" + opportunities
        )

        self.context["roadmap"] = roadmap

        return self.context