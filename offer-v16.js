'use strict';
// The primary v13 script applies the service query parameter first.
(() => {
  const scope = new URLSearchParams(location.search).get('scope');
  if (['0','1','2'].includes(scope)) {
    document.querySelectorAll('.split a.button').forEach(a => {
      const url = new URL(a.href);
      url.searchParams.set('scope',scope);
      a.href = url.toString();
    });
  }
  const select = document.querySelector('select[name="service"]');
  const box = document.querySelector('.service-context');
  const choice = new URLSearchParams(location.search).get('choice');
  if (select && /^\d+$/.test(choice || '') && select.options[Number(choice)]) select.selectedIndex = Number(choice);
  const languageLinks = () => document.querySelectorAll('.langs a').forEach(a => {
    const url = new URL(a.href);
    if (['0','1','2'].includes(scope)) url.searchParams.set('scope', scope);
    if (select && select.selectedIndex > 0) url.searchParams.set('choice', String(select.selectedIndex));
    else url.searchParams.delete('choice');
    url.searchParams.delete('service');
    a.href = url.toString();
  });
  languageLinks();
  if (!select || !box) return;
  if (!choice && !new URLSearchParams(location.search).has('service') && ['0','1','2'].includes(scope)) {
    const options = [...select.querySelectorAll('option[data-kind="new"]')];
    if (options[Number(scope)]) select.value = options[Number(scope)].value;
  }
  const refresh = () => {
    languageLinks();
    const kind = select.selectedOptions[0]?.dataset.kind || 'neutral';
    box.querySelectorAll('[data-context]').forEach(p => { p.hidden = p.dataset.context !== kind; });
    const link = box.querySelector('a');
    if (link) link.hidden = kind === 'new';
  };
  select.addEventListener('change', refresh);
  addEventListener('pageshow', refresh);
  refresh();
})();
