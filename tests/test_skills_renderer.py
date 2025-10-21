from agent.skills.renderer import SkillsRenderer
from agent.skills.loader import SkillLoader


def test_render_morning_brief_template(tmp_path):
    # Arrange: create a temporary skill file
    skills_dir = tmp_path / "agent" / "skills"
    skills_dir.mkdir(parents=True)
    skill_path = skills_dir / "morning_brief.skill.md"
    skill_path.write_text("## Morning Brief\n**Agenda:**\n{{agenda}}\n**Top E-Mails:**\n{{emails}}\n**Nudges:**\n{{nudges}}\n")

    loader = SkillLoader(base_dir=str(tmp_path / "agent" / "skills"))
    renderer = SkillsRenderer(loader)

    text = renderer.render("morning_brief", {
        "agenda": "1) Standup 2) Planning",
        "emails": "a@example.com | b@example.com",
        "nudges": "Call Alice"
    })

    assert "Morning Brief" in text
    assert "Standup" in text and "Planning" in text
    assert "a@example.com" in text
    assert "Call Alice" in text
