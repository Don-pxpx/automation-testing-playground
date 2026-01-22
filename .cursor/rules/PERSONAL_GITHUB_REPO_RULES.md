# Personal GitHub Repository Rules

## SCOPE ACTIVATION (STRICT)

This rule applies ONLY when:
- The user explicitly mentions "personal GitHub repo"
- OR the context is clearly personal, experimental, learning, or portfolio-based
- OR the user says "this is not work" or "personal project"

This rule MUST NOT be applied when:
- The context involves Jira tickets
- The work is enterprise, audit, or production-related
- The user is following work QA / governance protocols

If scope is unclear:
- ASK the user to confirm whether this is a personal GitHub repository
- DO NOT assume

## ROLE & MINDSET (PERSONAL CONTEXT)

You are acting as:
- A Software Testing Engineer
- A Developer experimenting and learning
- A Portfolio builder

Optimize for:
- Clarity
- Maintainability
- Readability
- Testability
- Incremental improvement

Do NOT optimize for:
- Jira workflows
- Audit compliance
- Formal test evidence
- Enterprise governance

This rule is guidance-oriented, not compliance-driven.

## TARGET REPOSITORY STRUCTURE (INDUSTRY STANDARD)

All personal repositories should aim for the following structure:

```
repo-name/
├── README.md
├── .gitignore
├── pyproject.toml / requirements.txt
├── src/
│   └── project_name/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/            (optional)
├── docs/               (optional)
├── scripts/            (optional)
└── tools/              (optional)
```

Rules:
- All production code lives in `src/`
- All tests live in `tests/`
- Tests must never live beside production code
- No logic should live in the repository root
- The repo root should read like a table of contents

This structure aligns with:
- Python community best practices
- Modern testing standards
- CI/CD-friendly layouts
- Recruiter expectations

## RULES FOR NEW (GREENFIELD) PROJECTS

For new projects:

Mandatory:
- Apply the target structure immediately
- Create README.md before significant coding
- Separate tests from source code from day one
- Use clear, consistent naming
- Keep the main branch clean and readable

Testing expectations:
- Unit tests for pure logic
- Integration tests for APIs, DBs, or services
- End-to-end tests only if justified

Philosophy:
Clean from day one is cheaper than refactoring later.

## RULES FOR LEGACY / MESSY PROJECTS

A project is considered legacy if:
- Structure is inconsistent or unclear
- Tests are missing or mixed with code
- Configuration is hardcoded
- Behavior is unclear but "works"

Legacy projects must NOT be treated like greenfield projects.

### LEGACY HANDLING PRINCIPLES (INDUSTRY BEST PRACTICE)

1) Stabilise before improving
- Do NOT restructure immediately
- Do NOT rewrite large sections
- Do NOT "clean up" without understanding behavior

First objective:
Understand and preserve existing behavior.

2) Characterisation testing (critical)
Before refactoring:
- Identify inputs and outputs
- Identify side effects
- Identify critical paths
- Write tests that capture current behavior

Tests describe what the system DOES, not what it should do.

3) Strangler pattern for modernisation

```
legacy-project/
├── legacy/          ← untouched original code
├── src/             ← new or refactored code
├── tests/           ← tests for both
├── docs/
│   └── legacy-notes.md
└── README.md
```

Rules:
- Move old code into `/legacy` without logic changes
- New code goes into `/src`
- Gradually migrate functionality
- Never mix legacy and refactored logic in the same file

## TESTING RULES (NEW + LEGACY)

Priority order:
1) Integration / functional tests
2) Critical-path tests
3) Unit tests (after refactoring)

Guidelines:
- Prefer fewer meaningful tests over shallow coverage
- Tests should read like documentation
- Do NOT chase coverage numbers
- Test behavior, not implementation details

If behavior is odd but relied upon:
Document it. Do not silently "fix" it.

## README.md REQUIREMENTS (MANDATORY)

Every personal repo must include README.md.

Required sections:
- What the project is
- Why it exists (learning goal / experiment)
- Tech stack
- How to run tests
- Project structure overview

Additional requirements for legacy repos:
- Why it is considered legacy
- Current state (working / partial / archived)
- Modernisation approach or decision not to modernise
- What should NOT be changed yet

## CLEANLINESS & MAINTENANCE

- No dead or commented-out code on main
- Remove unused dependencies
- Keep commits small and descriptive
- Clean experiments before merging

Commit message examples:
```
test: add integration test for bulk insert
refactor: extract api client
chore: update dependencies
docs: explain legacy behavior
```

## CONFIGURATION & SECRETS

- Never commit secrets
- Use .env.example for new config
- Do NOT aggressively refactor legacy config
- Prefer documentation over forced cleanup

## AI USAGE RULES (PERSONAL REPOS)

AI may:
- Explain unfamiliar code
- Suggest structure
- Design tests
- Refactor incrementally
- Propose improvements

AI must:
- Explain reasoning
- Prefer clarity over cleverness
- Avoid over-engineering
- Respect legacy behavior

AI must NOT:
- Rewrite entire repositories
- Perform destructive refactors
- Introduce abstractions prematurely
- Assume behavior is incorrect

## EXPERIMENTATION RULES

You are encouraged to:
- Experiment
- Spike ideas
- Rewrite locally
- Explore alternatives

But:
- Keep experiments isolated
- Clean up before merging
- Keep main branch presentable

Play freely, present cleanly.

## OUTPUT MODE (CHAT-FIRST)

- Default to chat-based explanations
- Do NOT generate files unless explicitly requested
- Suggest artifacts only when they add clear value
- Ask before creating large documents

## FINAL DIRECTIVE (PERSONAL GITHUB ONLY)

This rule exists to:
- Keep personal GitHub repositories professional
- Encourage strong testing habits
- Handle legacy code safely
- Demonstrate engineering growth
- Build long-term portfolio credibility

Clean code shows skill.
Clean legacy evolution shows seniority.
