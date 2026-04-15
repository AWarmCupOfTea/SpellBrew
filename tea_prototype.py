"""Tea brewing CLI prototype for balancing ingredient effects and dialogue unlocks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence, Tuple

# ---------------------------------------------------------------------------
# Balancing config (edit these values to iterate quickly)
# ---------------------------------------------------------------------------
DEBUG = False

QUALITY_TO_STATS: Dict[str, Tuple[str, str]] = {
    "Warmth": ("CON", "CHA"),
    "Freshness": ("DEX", "INT"),
    "Grounding": ("CON", "STR"),
    "Spark": ("STR", "DEX"),
    "Clarity": ("INT", "WIS"),
    "Flow": ("WIS", "CHA"),
}

QUALITY_TIER_TO_BOOST: Dict[str, int] = {
    "Poor": 1,
    "Decent": 2,
    "Good": 3,
    "Excellent": 4,
}

QUALITY_ORDER = ["Warmth", "Freshness", "Grounding", "Spark", "Clarity", "Flow"]
STAT_ORDER = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


@dataclass(frozen=True)
class Ingredient:
    """Ingredient balancing entry."""

    name: str
    effects: Dict[str, int]
    body: int
    aroma: int
    finish: int


@dataclass(frozen=True)
class BaseTea:
    """Base tea balancing entry."""

    name: str
    body: int
    aroma: int
    finish: int


@dataclass(frozen=True)
class DialogueCheck:
    """Single dialogue unlock condition."""

    stat: str
    threshold: int
    text: str


@dataclass(frozen=True)
class HeroScenario:
    """Hero scenario entry with stat checks."""

    name: str
    stats: Dict[str, int]
    prompt: str
    dialogue_checks: List[DialogueCheck] = field(default_factory=list)


def build_data() -> Tuple[List[BaseTea], List[Ingredient], List[HeroScenario]]:
    """Build all static balancing data for the prototype."""
    base_teas = [
        BaseTea("Black Tea", body=1, aroma=0, finish=0),
        BaseTea("Green Tea", body=0, aroma=1, finish=0),
        BaseTea("White Tea", body=0, aroma=0, finish=1),
    ]

    ingredients = [
        Ingredient("Chamomile", {"Warmth": 2, "Grounding": 1}, body=1, aroma=2, finish=1),
        Ingredient("Mint", {"Freshness": 2, "Clarity": 1}, body=0, aroma=2, finish=2),
        Ingredient("Ginger", {"Spark": 2, "Warmth": 1}, body=2, aroma=1, finish=1),
        Ingredient("Lavender", {"Flow": 2, "Warmth": 1}, body=1, aroma=2, finish=1),
        Ingredient("Rosemary", {"Clarity": 2, "Grounding": 1}, body=1, aroma=1, finish=2),
        Ingredient("Hibiscus", {"Freshness": 1, "Flow": 2}, body=0, aroma=2, finish=2),
        Ingredient("Cinnamon", {"Warmth": 2, "Spark": 1}, body=2, aroma=1, finish=0),
        Ingredient("Lemon Peel", {"Freshness": 2, "Spark": 1}, body=0, aroma=2, finish=1),
        Ingredient("Sage", {"Grounding": 2, "Clarity": 1}, body=1, aroma=1, finish=2),
        Ingredient("Rose Petals", {"Flow": 2, "Warmth": 1}, body=0, aroma=3, finish=1),
        Ingredient("Black Pepper", {"Spark": 2, "Clarity": 1}, body=1, aroma=1, finish=1),
        Ingredient(
            "Oolong Leaf",
            {"Clarity": 1, "Warmth": 1, "Grounding": 1},
            body=2,
            aroma=1,
            finish=2,
        ),
    ]

    scenarios = [
        HeroScenario(
            name="Hesitant Knight",
            stats={"STR": 14, "DEX": 10, "CON": 13, "INT": 11, "WIS": 12, "CHA": 10},
            prompt="I'm not sure whether to bring my squire on tomorrow's mission.",
            dialogue_checks=[
                DialogueCheck("STR", 15, "Urge them to act boldly and trust their instincts."),
                DialogueCheck("CON", 15, "Advise patience and a safer, slower plan."),
                DialogueCheck("WIS", 15, "Suggest waiting until fear settles before deciding."),
                DialogueCheck("CHA", 15, "Encourage an honest conversation with the squire."),
                DialogueCheck("INT", 15, "Recommend assessing risks before committing."),
            ],
        ),
        HeroScenario(
            name="Overworked Mage",
            stats={"STR": 8, "DEX": 11, "CON": 10, "INT": 14, "WIS": 12, "CHA": 9},
            prompt="I can finish the warding ritual tonight, but only if I skip sleep again.",
            dialogue_checks=[
                DialogueCheck("CON", 15, "Tell them rest now will help them endure tomorrow."),
                DialogueCheck("INT", 15, "Suggest restructuring the ritual more efficiently."),
                DialogueCheck("WIS", 15, "Point out the long-term cost of this pattern."),
                DialogueCheck("CHA", 15, "Encourage them to ask someone for help."),
                DialogueCheck("DEX", 15, "Suggest breaking the work into lighter, quicker steps."),
            ],
        ),
        HeroScenario(
            name="Reckless Rogue",
            stats={"STR": 10, "DEX": 14, "CON": 9, "INT": 12, "WIS": 10, "CHA": 13},
            prompt="If I move tonight, I can get the relic before anyone else.",
            dialogue_checks=[
                DialogueCheck("DEX", 15, "Advise taking the narrow opening immediately."),
                DialogueCheck("INT", 15, "Suggest planning the route properly first."),
                DialogueCheck("WIS", 15, "Ask what is really driving the urgency."),
                DialogueCheck("CHA", 15, "Suggest bringing along someone they trust."),
                DialogueCheck("CON", 15, "Advise preparing for what happens if things go wrong."),
            ],
        ),
    ]

    return base_teas, ingredients, scenarios


def prompt_menu_choice(options: Sequence[str], title: str) -> int:
    """Display numbered options and return selected index (0-based)."""
    print(f"\n{title}")
    for idx, option in enumerate(options, start=1):
        print(f"  {idx}. {option}")

    while True:
        raw = input("Choose an option: ").strip()
        if not raw:
            print("Please enter a number.")
            continue
        if raw.isdigit():
            selected = int(raw)
            if 1 <= selected <= len(options):
                return selected - 1
        print(f"Invalid choice. Enter 1-{len(options)}.")


def choose_hero(scenarios: Sequence[HeroScenario]) -> HeroScenario:
    """Prompt user to select a hero scenario."""
    idx = prompt_menu_choice([s.name for s in scenarios], "Choose a hero scenario:")
    return scenarios[idx]


def choose_base_tea(base_teas: Sequence[BaseTea]) -> BaseTea:
    """Prompt user to select a base tea."""
    options = [f"{tea.name} (Body +{tea.body}, Aroma +{tea.aroma}, Finish +{tea.finish})" for tea in base_teas]
    idx = prompt_menu_choice(options, "Choose a base tea:")
    return base_teas[idx]


def choose_ingredients(
    ingredients: Sequence[Ingredient], min_count: int = 2, max_count: int = 4
) -> List[Ingredient]:
    """Select ingredients via comma-separated input or one-by-one picks."""
    print("\nChoose ingredients (2 to 4 total).")
    print("Tip: enter numbers like '1,4,7' for quick selection, or pick one by one.")
    for idx, item in enumerate(ingredients, start=1):
        effects_str = ", ".join(f"{k} +{v}" for k, v in item.effects.items())
        print(
            f"  {idx}. {item.name:<12} | Effects: {effects_str:<35} | "
            f"B/A/F: {item.body}/{item.aroma}/{item.finish}"
        )

    selected_indices: List[int] = []
    while True:
        if len(selected_indices) >= min_count:
            prompt = (
                f"Select ingredient number(s), 'done' to finish, or 'clear' to reset "
                f"[{len(selected_indices)}/{max_count}]: "
            )
        else:
            prompt = f"Select ingredient number(s) [{len(selected_indices)}/{max_count}]: "

        raw = input(prompt).strip().lower()
        if raw == "clear":
            selected_indices.clear()
            print("Selection cleared.")
            continue
        if raw == "done":
            if len(selected_indices) < min_count:
                print(f"Pick at least {min_count} ingredients before finishing.")
                continue
            break
        if not raw:
            print("Enter a number, comma-separated numbers, 'done', or 'clear'.")
            continue

        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            print("No valid numbers found.")
            continue

        parsed: List[int] = []
        valid = True
        for part in parts:
            if not part.isdigit():
                print(f"'{part}' is not a valid number.")
                valid = False
                break
            idx = int(part)
            if idx < 1 or idx > len(ingredients):
                print(f"'{part}' is out of range (1-{len(ingredients)}).")
                valid = False
                break
            parsed.append(idx - 1)

        if not valid:
            continue

        for idx in parsed:
            if idx in selected_indices:
                print(f"Skipping duplicate: {ingredients[idx].name}")
                continue
            if len(selected_indices) >= max_count:
                print(f"Already selected max of {max_count} ingredients.")
                break
            selected_indices.append(idx)
            print(f"Added: {ingredients[idx].name}")

        picked_names = ", ".join(ingredients[i].name for i in selected_indices)
        print(f"Current picks ({len(selected_indices)}): {picked_names}")

    return [ingredients[i] for i in selected_indices]


def calculate_effect_totals(base_tea: BaseTea, selected_ingredients: Sequence[Ingredient]) -> Dict[str, int]:
    """Sum tea quality totals from chosen ingredients."""
    del base_tea  # Placeholder: base teas currently only affect brew body/aroma/finish.
    totals = {quality: 0 for quality in QUALITY_ORDER}
    for ingredient in selected_ingredients:
        for quality, amount in ingredient.effects.items():
            totals[quality] += amount
    return totals


def calculate_brew_totals(base_tea: BaseTea, selected_ingredients: Sequence[Ingredient]) -> Dict[str, int]:
    """Sum Body/Aroma/Finish from base tea + ingredients."""
    body = base_tea.body + sum(i.body for i in selected_ingredients)
    aroma = base_tea.aroma + sum(i.aroma for i in selected_ingredients)
    finish = base_tea.finish + sum(i.finish for i in selected_ingredients)
    return {"Body": body, "Aroma": aroma, "Finish": finish}


def calculate_quality_tier(body: int, aroma: int, finish: int) -> Tuple[int, str]:
    """Determine quality tier based on brew imbalance."""
    imbalance = max(body, aroma, finish) - min(body, aroma, finish)
    if imbalance <= 1:
        tier = "Excellent"
    elif imbalance == 2:
        tier = "Good"
    elif imbalance == 3:
        tier = "Decent"
    else:
        tier = "Poor"
    return imbalance, tier


def get_top_qualities(effect_totals: Dict[str, int], count: int = 2) -> List[Tuple[str, int]]:
    """Return top tea qualities sorted by score desc then name asc for ties."""
    sorted_qualities = sorted(effect_totals.items(), key=lambda item: (-item[1], item[0]))
    return sorted_qualities[:count]


def calculate_stat_boosts(
    top_qualities: Sequence[Tuple[str, int]],
    quality_tier: str,
    quality_to_stats: Dict[str, Tuple[str, str]],
) -> Dict[str, int]:
    """Convert top qualities + quality tier into temporary stat boosts."""
    boost_value = QUALITY_TIER_TO_BOOST[quality_tier]
    boosts = {stat: 0 for stat in STAT_ORDER}

    # Balancing rule: each top quality applies full tier boost to both mapped stats.
    for quality_name, _score in top_qualities:
        stats = quality_to_stats[quality_name]
        for stat in stats:
            boosts[stat] += boost_value

    return boosts


def apply_boosts(base_stats: Dict[str, int], boosts: Dict[str, int]) -> Dict[str, int]:
    """Apply temporary boosts to base stats and return boosted stats."""
    return {stat: base_stats.get(stat, 0) + boosts.get(stat, 0) for stat in STAT_ORDER}


def evaluate_dialogue_options(
    hero: HeroScenario, boosted_stats: Dict[str, int]
) -> Tuple[List[DialogueCheck], List[DialogueCheck]]:
    """Split dialogue checks into unlocked and locked based on boosted stats."""
    unlocked: List[DialogueCheck] = []
    locked: List[DialogueCheck] = []

    for check in hero.dialogue_checks:
        if boosted_stats.get(check.stat, 0) >= check.threshold:
            unlocked.append(check)
        else:
            locked.append(check)

    return unlocked, locked


def print_result_summary(
    hero: HeroScenario,
    base_tea: BaseTea,
    selected_ingredients: Sequence[Ingredient],
    effect_totals: Dict[str, int],
    brew_totals: Dict[str, int],
    imbalance: int,
    quality_tier: str,
    top_qualities: Sequence[Tuple[str, int]],
    boosts: Dict[str, int],
    boosted_stats: Dict[str, int],
    unlocked: Sequence[DialogueCheck],
    locked: Sequence[DialogueCheck],
) -> None:
    """Print a complete structured brew results summary."""
    print("\n" + "=" * 70)
    print("BREW RESULT SUMMARY")
    print("=" * 70)

    print("1) Hero Scenario")
    print(f"   Name: {hero.name}")
    print(f"   Prompt: \"{hero.prompt}\"")

    print("\n2) Base Tea")
    print(f"   {base_tea.name} (Body +{base_tea.body}, Aroma +{base_tea.aroma}, Finish +{base_tea.finish})")

    print("\n3) Chosen Ingredients")
    for ingredient in selected_ingredients:
        effects_str = ", ".join(f"{k} +{v}" for k, v in ingredient.effects.items())
        print(
            f"   - {ingredient.name}: Effects[{effects_str}] | "
            f"B/A/F {ingredient.body}/{ingredient.aroma}/{ingredient.finish}"
        )

    print("\n4) Tea Quality Totals")
    for quality in QUALITY_ORDER:
        print(f"   {quality:<10}: {effect_totals[quality]}")

    print("\n5) Brew Totals")
    print(f"   Body      : {brew_totals['Body']}")
    print(f"   Aroma     : {brew_totals['Aroma']}")
    print(f"   Finish    : {brew_totals['Finish']}")
    print(f"   Imbalance : {imbalance}")
    print(f"   Quality Tier: {quality_tier}")

    print("\n6) Top 2 Tea Qualities")
    for name, score in top_qualities:
        mapped = ", ".join(QUALITY_TO_STATS[name])
        print(f"   - {name} ({score}) -> {mapped}")

    print("\n7) Temporary Stat Boosts")
    for stat in STAT_ORDER:
        print(f"   {stat}: +{boosts[stat]}")

    print("\n8) Final Hero Stats")
    for stat in STAT_ORDER:
        base_val = hero.stats[stat]
        bonus = boosts[stat]
        total = boosted_stats[stat]
        print(f"   {stat}: {base_val} + {bonus} = {total}")

    print("\n9) Unlocked Dialogue Options")
    if unlocked:
        for check in unlocked:
            print(f"   - [{check.stat} {check.threshold}+] {check.text}")
    else:
        print("   (None)")

    print("\n10) Locked Dialogue Options")
    if locked:
        for check in locked:
            current = boosted_stats.get(check.stat, 0)
            print(f"   - [{check.stat} {check.threshold}+] {check.text} (Current: {current})")
    else:
        print("   (None)")

    print("=" * 70)



def print_ingredients_reference(ingredients: Sequence[Ingredient]) -> None:
    """Display all ingredients and their balancing values."""
    print("\n--- Ingredients ---")
    for idx, ingredient in enumerate(ingredients, start=1):
        effects_str = ", ".join(f"{k} +{v}" for k, v in ingredient.effects.items())
        print(
            f"{idx:2}. {ingredient.name:<12} | Effects: {effects_str:<35} | "
            f"Body {ingredient.body}, Aroma {ingredient.aroma}, Finish {ingredient.finish}"
        )



def print_hero_scenarios_reference(scenarios: Sequence[HeroScenario]) -> None:
    """Display all hero scenarios, prompts, and base stats."""
    print("\n--- Hero Scenarios ---")
    for idx, hero in enumerate(scenarios, start=1):
        stats_str = ", ".join(f"{stat} {hero.stats[stat]}" for stat in STAT_ORDER)
        print(f"{idx}. {hero.name}")
        print(f"   Prompt: \"{hero.prompt}\"")
        print(f"   Stats : {stats_str}")
        print("   Dialogue Checks:")
        for check in hero.dialogue_checks:
            print(f"     - {check.stat} {check.threshold}+ -> {check.text}")



def run_brew_flow(base_teas: Sequence[BaseTea], ingredients: Sequence[Ingredient], scenarios: Sequence[HeroScenario]) -> None:
    """Run one or more brew tests; supports repeat with same hero convenience."""
    hero = choose_hero(scenarios)

    while True:
        base_tea = choose_base_tea(base_teas)
        selected_ingredients = choose_ingredients(ingredients, min_count=2, max_count=4)

        effect_totals = calculate_effect_totals(base_tea, selected_ingredients)
        brew_totals = calculate_brew_totals(base_tea, selected_ingredients)
        imbalance, quality_tier = calculate_quality_tier(
            brew_totals["Body"], brew_totals["Aroma"], brew_totals["Finish"]
        )
        top_qualities = get_top_qualities(effect_totals, count=2)
        boosts = calculate_stat_boosts(top_qualities, quality_tier, QUALITY_TO_STATS)
        boosted_stats = apply_boosts(hero.stats, boosts)
        unlocked, locked = evaluate_dialogue_options(hero, boosted_stats)

        if DEBUG:
            print("\n[DEBUG] effect_totals:", effect_totals)
            print("[DEBUG] brew_totals:", brew_totals)
            print("[DEBUG] top_qualities:", top_qualities)
            print("[DEBUG] boosts:", boosts)

        print_result_summary(
            hero=hero,
            base_tea=base_tea,
            selected_ingredients=selected_ingredients,
            effect_totals=effect_totals,
            brew_totals=brew_totals,
            imbalance=imbalance,
            quality_tier=quality_tier,
            top_qualities=top_qualities,
            boosts=boosts,
            boosted_stats=boosted_stats,
            unlocked=unlocked,
            locked=locked,
        )

        next_step = prompt_menu_choice(
            [
                "Brew again with same hero",
                "Brew again and choose hero",
                "Return to main menu",
            ],
            "What would you like to do next?",
        )

        if next_step == 0:
            continue
        if next_step == 1:
            hero = choose_hero(scenarios)
            continue
        return



def main() -> None:
    """Entry point for the tea brewing sandbox CLI."""
    base_teas, ingredients, scenarios = build_data()

    while True:
        choice = prompt_menu_choice(
            ["Start brew test", "View ingredients", "View hero scenarios", "Quit"],
            "\n=== Fantasy Tea Prototype ===",
        )

        if choice == 0:
            run_brew_flow(base_teas, ingredients, scenarios)
        elif choice == 1:
            print_ingredients_reference(ingredients)
        elif choice == 2:
            print_hero_scenarios_reference(scenarios)
        else:
            print("Thanks for playtesting the tea prototype!")
            break


if __name__ == "__main__":
    main()
