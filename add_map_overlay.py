import os
from pathlib import Path

# Папки предметов (куда добавляем кнопку карты)
SUBJECT_FOLDERS = ["historykaz", "worldhistory", "geography"]

POSTERS_ROOT = Path("content/posters")
MAPS_ROOT = Path("content/assets/maps")

INJECT_MARK = "data-oi-map-overlay"

ALL_MAP_FILES = ["karta_1.png", "karta_2.png", "karta_3.png", "karta_4.png"]

CSS = """
<style data-oi-map-overlay>
.oi-map-btn{
  position:fixed; right:16px; bottom:16px; z-index:9999;
  padding:10px 14px; border-radius:999px; border:1px solid rgba(0,0,0,.15);
  background:#fff; cursor:pointer; font:600 14px/1.1 system-ui,-apple-system,Segoe UI,Roboto,Arial;
  box-shadow:0 8px 20px rgba(0,0,0,.12);
}
.oi-map-backdrop{
  position:fixed; inset:0; background:rgba(0,0,0,.72); z-index:10000;
  display:none; align-items:center; justify-content:center; padding:18px;
}
.oi-map-backdrop[aria-hidden="false"]{ display:flex; }
.oi-map-modal{
  width:min(1100px, 100%); height:min(85vh, 900px);
  background:#111; border-radius:14px; overflow:hidden; position:relative;
  box-shadow:0 20px 60px rgba(0,0,0,.35);
}
.oi-map-close{
  position:absolute; top:10px; right:10px; z-index:3;
  width:40px; height:40px; border-radius:999px; border:1px solid rgba(255,255,255,.25);
  background:rgba(0,0,0,.35); color:#fff; cursor:pointer; font-size:22px;
}
.oi-map-viewport{
  width:100%; height:100%; overflow:auto; -webkit-overflow-scrolling:touch;
  touch-action: pan-x pan-y;
  background:#000;
  padding-top:56px; /* место под тулбар */
}
.oi-map-img{
  display:block;
  transform-origin: 0 0;
  user-select:none; -webkit-user-drag:none;
}
.oi-map-toolbar{
  position:absolute; left:12px; top:12px; right:12px; z-index:2;
  display:flex; align-items:center; justify-content:space-between; gap:10px;
  pointer-events:none;
}
.oi-map-tabs{ display:flex; gap:8px; pointer-events:auto; }
.oi-map-tab{
  width:36px; height:34px; border-radius:10px;
  border:1px solid rgba(255,255,255,.22);
  background:rgba(0,0,0,.35); color:#fff;
  cursor:pointer; font:600 14px system-ui,-apple-system,Segoe UI,Roboto,Arial;
}
.oi-map-tab.is-active{
  background:rgba(255,255,255,.12);
  border-color: rgba(255,255,255,.45);
}
.oi-map-hint{
  pointer-events:none;
  color:#fff; opacity:.85; font:12px/1.2 system-ui,-apple-system,Segoe UI,Roboto,Arial;
  background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.18);
  padding:8px 10px; border-radius:10px;
}
</style>
"""

JS = """
<script data-oi-map-overlay>
(function(){
  const btn = document.querySelector('[data-oi-map-btn]');
  const backdrop = document.querySelector('[data-oi-map-backdrop]');
  const closeBtn = document.querySelector('[data-oi-map-close]');
  const viewport = document.querySelector('[data-oi-map-viewport]');
  const tabs = Array.from(document.querySelectorAll('[data-oi-map-tab]'));
  const imgs = Array.from(document.querySelectorAll('[data-oi-map-img][data-map]'));
  if(!btn || !backdrop || !closeBtn || !viewport || imgs.length === 0) return;

  let scale = 1;

  function applyScale(){
    imgs.forEach(img => { img.style.transform = `scale(${scale})`; });
  }
  function openMap(){
    backdrop.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
  }
  function closeMap(){
    backdrop.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
  }
  function showMap(n){
    imgs.forEach(img => {
      img.style.display = (img.getAttribute('data-map') === String(n)) ? 'block' : 'none';
    });
    tabs.forEach(t => t.classList.toggle('is-active', t.getAttribute('data-oi-map-tab') === String(n)));
    viewport.scrollTop = 0;
    viewport.scrollLeft = 0;
  }

  btn.addEventListener('click', openMap);
  closeBtn.addEventListener('click', closeMap);
  backdrop.addEventListener('click', (e)=>{ if(e.target === backdrop) closeMap(); });
  window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeMap(); });

  tabs.forEach(t => t.addEventListener('click', () => showMap(t.getAttribute('data-oi-map-tab'))));

  viewport.addEventListener('wheel', (e)=>{
    if(backdrop.getAttribute('aria-hidden') !== 'false') return;
    e.preventDefault();
    const delta = -Math.sign(e.deltaY) * 0.1;
    scale = Math.min(4, Math.max(0.6, scale + delta));
    applyScale();
  }, {passive:false});

  applyScale();
  showMap(1);
})();
</script>
"""

def rel_web_path(from_dir: Path, target_file: Path) -> str:
    from_abs = from_dir.resolve()
    target_abs = target_file.resolve()
    rel = os.path.relpath(str(target_abs), str(from_abs))
    return rel.replace("\\", "/")

def build_inject(map_srcs: list[str]) -> str:
    imgs_html = "\n".join(
        f'<img class="oi-map-img" data-oi-map-img data-map="{i+1}" src="{src}" alt="Карта {i+1}" style="display:{"block" if i==0 else "none"};">'
        for i, src in enumerate(map_srcs)
    )
    return f"""
{CSS}
<button class="oi-map-btn" type="button" data-oi-map-btn>🗺️ Карта</button>

<div class="oi-map-backdrop" aria-hidden="true" data-oi-map-backdrop>
  <div class="oi-map-modal" role="dialog" aria-modal="true" aria-label="Карта">
    <button class="oi-map-close" type="button" aria-label="Закрыть" data-oi-map-close>×</button>

    <div class="oi-map-toolbar">
      <div class="oi-map-tabs">
        <button type="button" class="oi-map-tab is-active" data-oi-map-tab="1">1</button>
        <button type="button" class="oi-map-tab" data-oi-map-tab="2">2</button>
        <button type="button" class="oi-map-tab" data-oi-map-tab="3">3</button>
        <button type="button" class="oi-map-tab" data-oi-map-tab="4">4</button>
      </div>
      <div class="oi-map-hint">Колёсико/трекпад — зум • Esc — закрыть</div>
    </div>

    <div class="oi-map-viewport" data-oi-map-viewport>
      {imgs_html}
    </div>
  </div>
</div>

{JS}
""".strip()

def strip_old_overlay(text: str) -> str:
    # Удаляем любой предыдущий блок (CSS+JS) который мы вставляли раньше (по маркеру)
    # Чтобы всегда вставлять актуальную версию с вкладками.
    start = text.find('<style data-oi-map-overlay>')
    if start == -1:
        return text

    # Найдём конец последнего </script data-oi-map-overlay>
    # Мы вставляем <script data-oi-map-overlay> ... </script>
    end_script = text.rfind('</script>')
    if end_script == -1:
        return text

    # Очень безопасно: вырежем от начала <style data-oi-map-overlay> до конца </script> + чуть дальше, если там ещё наша разметка
    # Но мы хотим вырезать и кнопку+div. Поэтому вырежем от <style ...> до конца скрипта, а потом вычистим остатки по маркерным атрибутам.
    cut_end = end_script + len('</script>')
    chunk = text[start:cut_end]

    # Если в этом куске нет наших атрибутов — не трогаем
    if INJECT_MARK not in chunk and 'data-oi-map-btn' not in chunk and 'data-oi-map-backdrop' not in chunk:
        return text

    new_text = text[:start] + text[cut_end:]

    # подчистим остатки (кнопка/бекдроп), если они остались вне куска
    new_text = new_text.replace('<button class="oi-map-btn" type="button" data-oi-map-btn>🗺️ Карта</button>', '')
    # грубо удаляем бекдроп-блок (если остался)
    # найдём по маркеру data-oi-map-backdrop
    idx = new_text.find('data-oi-map-backdrop')
    if idx != -1:
        # попробуем удалить ближайший <div ...data-oi-map-backdrop...>...</div>
        # найдём начало div
        div_start = new_text.rfind('<div', 0, idx)
        if div_start != -1:
            # найдём закрывающий </div> для модалки. Это грубо, но работает для нашей вставки.
            div_end = new_text.find('</div>', idx)
            if div_end != -1:
                # удалим до пары закрывающих дивов (бекдроп включает вложенности)
                # лучше удалить до последнего </div> после idx
                last = new_text.find('</div>', div_end + 6)
                if last != -1:
                    new_text = new_text[:div_start] + new_text[last + 6:]

    return new_text

def inject_replace(path: Path, map_srcs: list[str]) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")

    # Если уже есть старая версия — вырежем и вставим новую
    if INJECT_MARK in text or 'data-oi-map-btn' in text or 'data-oi-map-overlay' in text:
        text2 = strip_old_overlay(text)
        inject = build_inject(map_srcs)
        if "</body>" in text2:
            text2 = text2.replace("</body>", inject + "\n</body>")
        else:
            text2 += "\n" + inject + "\n"
        path.write_text(text2, encoding="utf-8")
        return "replaced"

    # если блока нет — добавляем
    inject = build_inject(map_srcs)
    if "</body>" in text:
        text = text.replace("</body>", inject + "\n</body>")
    else:
        text += "\n" + inject + "\n"
    path.write_text(text, encoding="utf-8")
    return "injected"

def main():
    total = injected = replaced = 0

    # проверим наличие карт
    for mf in ALL_MAP_FILES:
        p = MAPS_ROOT / mf
        if not p.exists():
            print(f"❌ Нет файла карты: {p}")
            return

    for folder in SUBJECT_FOLDERS:
        subject_dir = POSTERS_ROOT / folder
        if not subject_dir.exists():
            print(f"⚠️ Нет папки предмета: {subject_dir}")
            continue

        for html_file in subject_dir.rglob("*.html"):
            total += 1
            map_srcs = [rel_web_path(html_file.parent, MAPS_ROOT / mf) for mf in ALL_MAP_FILES]
            res = inject_replace(html_file, map_srcs)
            if res == "injected":
                injected += 1
            else:
                replaced += 1

    print(f"✅ Готово. HTML: {total} | добавлено: {injected} | обновлено/заменено: {replaced}")

if __name__ == "__main__":
    main()
