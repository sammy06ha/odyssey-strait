# 작업 메모 (Claude용)

- 사이트: https://sammy06ha.github.io/odyssey-strait/ (GitHub Pages, main 브랜치 루트에서 배포)
- 사용자: 새미(한국어로 답하기). 26-2 청송하우스 닫는 모임 부스 6 「스퀼라와 카륍디스의 해협」 한 팀용 게임.
- 수정은 `src/template.html`(화면·연출)과 `src/data.js`(시련 20개·카드·퀴즈·미션)에서 하고, `python3 build.py`로 `index.html`을 다시 만든다. `index.html`을 직접 고치지 않는다.
- 빌드 뒤 확인: `<script>`를 뽑아 `node --check`, 가능하면 Playwright로 화면을 찍어 본다.
- 그림 파일: `img/`(명화, 퍼블릭 도메인), `art/`(Figma AI 스토리 그림), `icons/`(흑색상 도기 아이콘).
- 고란손 사운드트랙 등 저작권 음원은 저장소에 넣지 않는다. 행사 때는 설정의 "음악 파일 불러오기"로 재생.
- main에 바로 커밋하고 push하면 1분 안에 사이트에 반영된다.
