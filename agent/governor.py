class Governor:
    def __init__(self, default_tier: str = "TIER0_INFORM", kill_switch: bool = True):
        self.default_tier = default_tier
        self.kill_switch = kill_switch

    def current_tier(self) -> str:
        return self.default_tier

    def is_allowed(self, action: str, tier: str | None = None) -> bool:
        if self.kill_switch:
            return self.default_tier != "TIER2_ACT"
        return True
