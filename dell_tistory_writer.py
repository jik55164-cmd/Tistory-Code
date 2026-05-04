#!/usr/bin/env python3
"""티스토리용 델 테크놀로지 분석 글 생성기.

목표:
- 'AI가 쓴 티'를 줄이기 위해 고정 패턴 대신 여러 문단 구조를 조합
- 작성자의 실제 경험/주장/반론을 본문 핵심에 배치
- 단순 요약이 아닌 '수업/학습 가치'가 보이는 글 생성
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import argparse
import random


@dataclass
class WriterProfile:
    name: str
    audience: str
    tone: str
    teaching_context: str
    personal_take: str
    caution: str
    lived_scene: str
    disagree_point: str


@dataclass
class DellSnapshot:
    focus: str
    strengths: list[str]
    risks: list[str]
    classroom_examples: list[str]
    evidence_slots: list[str] = field(default_factory=list)


OPENERS = [
    "처음 델을 다시 보게 된 건, 단순히 PC 회사라는 인식이 깨진 순간부터였습니다.",
    "솔직히 말하면 예전의 저는 델을 '기업용 노트북 회사' 정도로만 봤습니다.",
    "최근 수업 자료를 준비하며 델을 다시 뜯어보니, 예상보다 훨씬 전략적인 회사였습니다.",
]

MIDDLE_BRIDGES = [
    "여기서 제 판단이 개입됩니다.",
    "숫자보다 먼저 봐야 할 장면이 있습니다.",
    "이 지점에서 시장 해석과 제 해석이 갈립니다.",
]

QUESTION_ENDINGS = [
    "여러분이라면 같은 데이터에서 어떤 결론을 내리실까요?",
    "같은 숫자를 보고도 다른 결론이 가능한데, 여러분의 기준은 무엇인가요?",
    "여기서 '좋은 회사'와 '좋은 투자'를 어떻게 구분하시겠습니까?",
]


POST_BLUEPRINTS = [
    [
        "hook",
        "thesis",
        "strength_risk_pair",
        "teaching_application",
        "counter_argument",
        "closing_question",
    ],
    [
        "hook",
        "scene",
        "thesis",
        "evidence_checklist",
        "teaching_application",
        "closing_question",
    ],
]


def p(text: str) -> str:
    return text.strip() + "\n\n"


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n\n"


def bullet(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def part_hook(profile: WriterProfile, _: DellSnapshot) -> str:
    return p(f"{random.choice(OPENERS)} 이번 글은 {profile.audience}에게 맞춰, {profile.teaching_context} 관점으로 씁니다.")


def part_scene(profile: WriterProfile, _: DellSnapshot) -> str:
    return section("제가 델을 다시 보기 시작한 실제 장면", p(profile.lived_scene))


def part_thesis(profile: WriterProfile, snap: DellSnapshot) -> str:
    body = p(
        f"제 핵심 주장은 간단합니다. 델을 볼 때는 '{snap.focus}'를 중심축으로 두고, "
        "매출 성장보다 반복 가능한 수익 구조를 먼저 확인해야 합니다."
    )
    body += p(f"{random.choice(MIDDLE_BRIDGES)} 과열 구간에서는 특히 {profile.caution}을 경계해야 합니다.")
    return section("이번 글의 주장", body)


def part_strength_risk_pair(_: WriterProfile, snap: DellSnapshot) -> str:
    body = "### 강점\n\n" + bullet([f"- {s}".replace("- -", "-") for s in snap.strengths]) + "\n\n"
    body += "### 동시에 보는 리스크\n\n" + bullet([f"- {r}".replace("- -", "-") for r in snap.risks]) + "\n\n"
    body += p("핵심은 '좋은 뉴스 1개'가 전체 추세를 대표한다고 착각하지 않는 것입니다.")
    return section("강점과 리스크를 한 화면에 놓고 보기", body)


def part_evidence_checklist(_: WriterProfile, snap: DellSnapshot) -> str:
    if not snap.evidence_slots:
        return ""
    body = p("아래 항목에 직접 숫자를 채우면 글이 훨씬 사람답고 신뢰도 있게 바뀝니다.")
    body += bullet([f"[체크] {slot}" for slot in snap.evidence_slots])
    return section("발행 전 숫자 검증 체크리스트", body)


def part_teaching_application(profile: WriterProfile, snap: DellSnapshot) -> str:
    body = p(
        f"{profile.name}님의 목적이 에드센스 승인과 학습 가치를 동시에 잡는 것이라면, "
        "'회사 소개'보다 '독자가 직접 써먹는 프레임'을 먼저 보여줘야 합니다."
    )
    body += bullet(snap.classroom_examples) + "\n\n"
    body += p("수업에서는 같은 사실을 낙관/중립/보수 관점으로 각각 3문장씩 재작성하게 하면 참여도가 올라갑니다.")
    return section("수업/콘텐츠 적용법", body)


def part_counter_argument(profile: WriterProfile, _: DellSnapshot) -> str:
    body = p(f"제가 동의하지 않는 흔한 주장: {profile.disagree_point}")
    body += p("반대 주장을 공정하게 소개한 뒤, 왜 동의하지 않는지 근거를 붙이면 글의 완성도가 확 올라갑니다.")
    body += p(f"개인 결론: {profile.personal_take}")
    return section("반론까지 포함한 개인 해석", body)


def part_closing_question(_: WriterProfile, __: DellSnapshot) -> str:
    return section("마무리 질문", p(random.choice(QUESTION_ENDINGS)))


PART_HANDLERS = {
    "hook": part_hook,
    "scene": part_scene,
    "thesis": part_thesis,
    "strength_risk_pair": part_strength_risk_pair,
    "evidence_checklist": part_evidence_checklist,
    "teaching_application": part_teaching_application,
    "counter_argument": part_counter_argument,
    "closing_question": part_closing_question,
}


def generate_post(profile: WriterProfile, snap: DellSnapshot, seed: int = 11, blueprint_index: int = 0) -> str:
    random.seed(seed)
    blueprint = POST_BLUEPRINTS[blueprint_index % len(POST_BLUEPRINTS)]

    pieces = ["# 델 테크놀로지 분석: 요약보다 판단이 남는 글\n\n"]
    for part_name in blueprint:
        part = PART_HANDLERS[part_name](profile, snap)
        if part.strip():
            pieces.append(part)

    pieces.append(f"_생성일: {date.today().isoformat()}_\n")
    return "".join(pieces)


def build_default_inputs() -> tuple[WriterProfile, DellSnapshot]:
    profile = WriterProfile(
        name="작성자",
        audience="초중급 투자/IT 독자",
        tone="분석적이되 대화형",
        teaching_context="수업 보조 자료",
        personal_take="델은 단기 테마보다 고객 락인 구조를 추적할 때 더 정확히 보입니다.",
        caution="AI 인프라 기대감만으로 멀티플을 정당화하는 해석",
        lived_scene="서로 다른 증권사 리포트 3개를 비교해보니, 같은 뉴스인데 결론이 완전히 달랐습니다.",
        disagree_point="'AI 수요가 늘면 하드웨어 업체는 자동으로 장기 성장한다'는 단정",
    )

    snapshot = DellSnapshot(
        focus="엔터프라이즈 인프라 + AI 서버 수요의 접점",
        strengths=[
            "기업 고객 기반이 두텁고 관계형 매출이 유지되는 구조",
            "서버·스토리지·서비스 결합 제안으로 객단가 방어 가능",
            "대형 프로젝트 대응을 위한 공급망 운영 경험 축적",
        ],
        risks=[
            "하드웨어 사이클 둔화 시 수요 공백이 실적 변동성으로 확대 가능",
            "AI 기대 과열 시 실수요와 밸류에이션 간 괴리 발생 가능",
            "가격/성능 경쟁 심화로 마진 압박 가능",
        ],
        classroom_examples=[
            "사례 1) '좋은 회사'와 '좋은 주식'의 차이를 델 밸류에이션 토론으로 구분",
            "사례 2) PC/서버/서비스를 분리해 매출의 질을 비교하는 과제 구성",
            "사례 3) 동일 뉴스 1개를 낙관·중립·보수 3관점으로 재작성",
        ],
        evidence_slots=[
            "직전 4개 분기 매출/영업이익 추이 (숫자 + 출처)",
            "인프라 솔루션 관련 매출 비중 변화",
            "AI 관련 발언이 실제 수주로 연결된 사례 1~2개",
        ],
    )
    return profile, snapshot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="델 분석 티스토리 글 생성기")
    parser.add_argument("--seed", type=int, default=11, help="문장 랜덤 시드")
    parser.add_argument("--blueprint", type=int, default=0, help="문단 구성 인덱스")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    profile_input, snapshot_input = build_default_inputs()
    print(generate_post(profile_input, snapshot_input, seed=args.seed, blueprint_index=args.blueprint))
