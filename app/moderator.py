class Moderator:
    """Decision aggregation for research only; never routes orders."""
    def review(self, arena_result):
        decisions=[x["decision"]["decision"] for x in arena_result.get("traders",[])]
        actionable=[d for d in decisions if d in ("BUY","SELL")]
        if not actionable: consensus="WAIT"
        elif actionable.count("BUY")>actionable.count("SELL"): consensus="BUY"
        elif actionable.count("SELL")>actionable.count("BUY"): consensus="SELL"
        else: consensus="CONFLICT"
        total=len(decisions) or 1
        agreement=max(actionable.count("BUY"),actionable.count("SELL"))/total if actionable else 0
        return {"consensus":consensus,"agreement":round(agreement,4),"votes":decisions,
                "mode":"PAPER","live_orders_enabled":False,
                "note":"Consensus is informational and not an execution instruction."}
