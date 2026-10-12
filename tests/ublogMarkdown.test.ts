import { initUblogMarkdown } from '../client/ublogMarkdown';

function renderBlogMarkdown(markdown: string): HTMLElement {
    document.body.innerHTML = `
        <textarea id="ublog-markdown-source"></textarea>
        <div id="ublog-markdown-render"></div>
    `;
    const source = document.getElementById('ublog-markdown-source') as HTMLTextAreaElement;
    source.value = markdown;
    initUblogMarkdown();
    return document.getElementById('ublog-markdown-render') as HTMLElement;
}

test('keeps youtube iframe embeds playable', () => {
    const root = renderBlogMarkdown(
        '<iframe width="560" height="315" src="https://www.youtube.com/embed/rz3f5febUAU" frameborder="0" allowfullscreen></iframe>',
    );
    const iframe = root.querySelector('iframe');
    expect(iframe).not.toBeNull();
    expect(iframe?.getAttribute('src')).toBe('https://www.youtube.com/embed/rz3f5febUAU');
    expect(iframe?.getAttribute('referrerpolicy')).toBe('strict-origin-when-cross-origin');
});

test('drops iframe embeds with unsafe src', () => {
    const root = renderBlogMarkdown('<iframe src="javascript:alert(1)"></iframe>');
    expect(root.querySelector('iframe')).toBeNull();
});

test.each([
    '</title><script>alert(document.cookie)</script>',
    '</title><img src="/missing-image" onerror="alert(document.cookie)">',
])('sanitizes malicious frontmatter title: %s', title => {
    const root = renderBlogMarkdown(`---\ntitle: ${title}\n---\n\n# Hello`);

    expect(root.querySelector('h1')?.textContent).toBe('Hello');
    // Frontmatter stays in the fragment instead of becoming document metadata.
    expect(root.textContent).toContain('title:');
    expect(root.querySelector('html, head, body, title, script, [onerror]')).toBeNull();
});

test.each(['"><svg/onload=alert(1)>', 'Name"/onmouseover="alert(1)'])(
    'sanitizes table header injection: %s',
    header => {
        const root = renderBlogMarkdown(`| ${header} | Col2 |\n| --- | --- |\n| Safe | Content |`);

        expect(root.querySelectorAll('th')).toHaveLength(2);
        expect(root.querySelectorAll('th')[1].textContent).toBe('Col2');
        expect(Array.from(root.querySelectorAll('td'), cell => cell.textContent)).toEqual(['Safe', 'Content']);
        expect(root.querySelector('svg, script, [id], [onload], [onmouseover]')).toBeNull();
    },
);
