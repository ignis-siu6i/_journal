<%*
const headingsGoFirst = ['/^goal$?', 'me', 'home', 'friend', 'work']
const filters = String.raw`not done
path does not include "_templates_/"`;
const tasksQuery = `${filters}
group by heading
group by tags
group by filename
sort by due
sort by priority`;

const firstBlock = (item) => String.raw`~~~tasks
heading matches regex ${item}
${tasksQuery}
~~~`;

const secondBlock = (item) => {
  const excludes = item.map(k => `heading does not include ${k}`).join('\n');
  return String.raw`~~~tasks
${excludes}
${tasksQuery}
~~~`;
};

const lines = [];
for (const item of headingsGoFirst) lines.push(firstBlock(item));
lines.push(secondBlock(headingsGoFirst))

tR += lines.join('\n\n\n');
%>