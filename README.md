# Tistory-Code

델 테크놀로지 분석 글을 티스토리에 올릴 때, **AI 요약문 느낌을 줄이고 개인 판단이 드러나는 문서**를 생성하기 위한 스크립트입니다.

## 실행

```bash
python3 dell_tistory_writer.py > post.md
```

다른 문단 구성으로 생성하려면:

```bash
python3 dell_tistory_writer.py --seed 24 --blueprint 1 > post_alt.md
```

## 무엇이 달라졌나

- 고정 양식 1개가 아니라 `POST_BLUEPRINTS`로 문단 순서를 바꿔 생성
- `lived_scene`, `disagree_point`, `personal_take`를 본문 핵심 섹션에 반영
- 발행 전 숫자를 직접 채울 수 있는 `evidence_slots` 체크리스트 제공

## 커스터마이징 포인트

`build_default_inputs()`의 다음 값을 본인 스타일로 바꾸세요.

- `WriterProfile.lived_scene`: 실제 경험 장면
- `WriterProfile.disagree_point`: 내가 동의하지 않는 시장 주장
- `WriterProfile.personal_take`: 최종 개인 결론
- `DellSnapshot.evidence_slots`: 실제 확인할 숫자/출처 슬롯

이 4가지를 본인 언어로 바꾸면, 같은 구조라도 글의 결이 크게 달라집니다.
