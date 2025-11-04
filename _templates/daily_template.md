# tasks
## 0. me

## 1. goal

## 2. home

## 3. fun +friends

## 4. work

<%*
/* 가장 심플: 매번 ZenQuotes 호출해서 한 줄 출력 */
try {
  const res = await request("https://zenquotes.io/api/random");
  const data = JSON.parse(res)[0]; // { q: "...", a: "..." }
  tR += `> [!quote] Today's quote\n> ${data.q}\n> — **${data.a}**`;
} catch (e) {
  tR += `> [!quote] Today's quote\n> Keep going.\n> — **Unknown**`;
}
%>