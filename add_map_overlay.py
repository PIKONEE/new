import os
from pathlib import Path

# Предметы, где нужны КАРТЫ
SUBJECT_FOLDERS = ["historykaz", "worldhistory", "geography"]

# Предмет, где нужна ТАБЛИЦА МЕНДЕЛЕЕВА
CHEMISTRY_FOLDER = "chemistry"

POSTERS_ROOT = Path("content/posters")
MAPS_ROOT = Path("content/assets/maps")

# Карты (1..N)
ALL_MAP_FILES = [
    "karta_1.png",
    "karta_2.png",
    "karta_3.png",
    "karta_4.png",
    "karta_5.png",
    "karta_6.png",
    "karta_7.png",
]

# Менделеев (1..2)
MENDELEEV_FILES = [
    "mendeleev_1.png",
    "mendeleev_2.png",
]

CSS = """
<style data-oi-map-overlay>
.oi-map-btn{
  position:fixed; right:16px; bottom:16px; z-index:9999;
  padding:10px 14px; border-radius:999px; border:1px solid rgba(0,0,0,.15);
  background:#fff; cursor:pointer; font:600 14px/1.1 system-ui,-apple-system,Segoe UI,Roboto,Arial;
  box-shadow:0 8px 20px rgba(0,0,0,.12);
}
.oi-table-btn{
  position:fixed; right:120px; bottom:16px; z-index:9999;
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
  width:min(1200px, 100%); height:min(85vh, 900px);
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
  padding-top:62px; /* место под тулбар */
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

.oi-map-tabs{ display:flex; gap:8px; flex-wrap:wrap; pointer-events:auto; }

.oi-map-tab{
  min-width:36px; height:34px; padding:0 10px;
  border-radius:10px;
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
  // ====== MAPS ======
  const mapBtn = document.querySelector('[data-oi-map-btn]');
  const mapBackdrop = document.querySelector('[data-oi-map-backdrop]');
  const mapCloseBtn = document.querySelector('[data-oi-map-close]');
  const mapViewport = document.querySelector('[data-oi-map-viewport]');
  const mapTabs = Array.from(document.querySelectorAll('[data-oi-map-tab]'));
  const mapImgs = Array.from(document.querySelectorAll('[data-oi-map-img][data-map]'));

  // ====== MENDELEEV ======
  const tableBtn = document.querySelector('[data-oi-table-btn]');
  const tableBackdrop = document.querySelector('[data-oi-table-backdrop]');
  const tableCloseBtn = document.querySelector('[data-oi-table-close]');
  const tableViewport = document.querySelector('[data-oi-table-viewport]');
  const tableTabs = Array.from(document.querySelectorAll('[data-oi-table-tab]'));
  const tableImgs = Array.from(document.querySelectorAll('[data-oi-table-img][data-table]'));

  let scale = 1;

  function applyScale(){
    mapImgs.forEach(img => { img.style.transform = `scale(${scale})`; });
    tableImgs.forEach(img => { img.style.transform = `scale(${scale})`; });
  }

  function openBackdrop(backdrop){
    backdrop.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
  }
  function closeBackdrop(backdrop){
    backdrop.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
  }

  function showMap(n){
    mapImgs.forEach(img => {
      img.style.display = (img.getAttribute('data-map') === String(n)) ? 'block' : 'none';
    });
    mapTabs.forEach(t => t.classList.toggle('is-active', t.getAttribute('data-oi-map-tab') === String(n)));
    if(mapViewport){ mapViewport.scrollTop = 0; mapViewport.scrollLeft = 0; }
  }

  function showTable(n){
    tableImgs.forEach(img => {
      img.style.display = (img.getAttribute('data-table') === String(n)) ? 'block' : 'none';
    });
    tableTabs.forEach(t => t.classList.toggle('is-active', t.getAttribute('data-oi-table-tab') === String(n)));
    if(tableViewport){ tableViewport.scrollTop = 0; tableViewport.scrollLeft = 0; }
  }

  // MAP events
  if(mapBtn && mapBackdrop && mapCloseBtn && mapViewport && mapImgs.length){
    mapBtn.addEventListener('click', () => openBackdrop(mapBackdrop));
    mapCloseBtn.addEventListener('click', () => closeBackdrop(mapBackdrop));
    mapBackdrop.addEventListener('click', (e)=>{ if(e.target === mapBackdrop) closeBackdrop(mapBackdrop); });
    window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeBackdrop(mapBackdrop); });
    mapTabs.forEach(t => t.addEventListener('click', () => showMap(t.getAttribute('data-oi-map-tab'))));

    mapViewport.addEventListener('wheel', (e)=>{
      if(mapBackdrop.getAttribute('aria-hidden') !== 'false') return;
      e.preventDefault();
      const delta = -Math.sign(e.deltaY) * 0.1;
      scale = Math.min(4, Math.max(0.6, scale + delta));
      applyScale();
    }, {passive:false});

    showMap(1);
  }

  // TABLE events
  if(tableBtn && tableBackdrop && tableCloseBtn && tableViewport && tableImgs.length){
    tableBtn.addEventListener('click', () => openBackdrop(tableBackdrop));
    tableCloseBtn.addEventListener('click', () => closeBackdrop(tableBackdrop));
    tableBackdrop.addEventListener('click', (e)=>{ if(e.target === tableBackdrop) closeBackdrop(tableBackdrop); });
    window.addEventListener('keydown', (e)=>{ if(e.key === 'Escape') closeBackdrop(tableBackdrop); });
    tableTabs.forEach(t => t.addEventListener('click', () => showTable(t.getAttribute('data-oi-table-tab'))));

    tableViewport.addEventListener('wheel', (e)=>{
      if(tableBackdrop.getAttribute('aria-hidden') !== 'false') return;
      e.preventDefault();
      const delta = -Math.sign(e.deltaY) * 0.1;
      scale = Math.min(4, Math.max(0.6, scale + delta));
      applyScale();
    }, {passive:false});

    showTable(1);
  }

  applyScale();
})();
</script>
"""

def rel_web_path(from_dir: Path, target_file: Path) -> str:
    from_abs = from_dir.resolve()
    target_abs = target_file.resolve()
    rel = os.path.relpath(str(target_abs), str(from_abs))
    return rel.replace("\\", "/")

def tabs_html(prefix: str, count: int) -> str:
    # prefix: "map" или "table"
    btns = []
    for i in range(1, count + 1):
        active = " is-active" if i == 1 else ""
        btns.append(f'<button type="button" class="oi-map-tab{active}" data-oi-{prefix}-tab="{i}">{i}</button>')
    return "\n".join(btns)

def imgs_html(attr_prefix: str, srcs: list[str]) -> str:
    # attr_prefix: "map" или "table"
    # data-map="1" / data-table="1"
    out = []
    for i, src in enumerate(srcs, start=1):
        display = "block" if i == 1 else "none"
        out.append(
            f'<img class="oi-map-img" data-oi-{attr_prefix}-img data-{attr_prefix}="{i}" '
            f'src="{src}" alt="{attr_prefix} {i}" style="display:{display};">'
        )
    return "\n".join(out)

def build_overlay(map_srcs: list[str], include_table: bool, table_srcs: list[str] | None = None) -> str:
    map_tabs = tabs_html("map", len(map_srcs))
    map_imgs = imgs_html("map", map_srcs)

    table_block = ""
    table_btn = ""
    if include_table:
        table_srcs = table_srcs or []
        table_tabs = tabs_html("table", len(table_srcs))
        table_imgs = imgs_html("table", table_srcs)

        table_btn = '<button class="oi-table-btn" type="button" data-oi-table-btn>🧪 Таблица</button>'

        table_block = f"""
<div class="oi-map-backdrop" aria-hidden="true" data-oi-table-backdrop>
  <div class="oi-map-modal" role="dialog" aria-modal="true" aria-label="Таблица Менделеева">
    <button class="oi-map-close" type="button" aria-label="Закрыть" data-oi-table-close>×</button>

    <div class="oi-map-toolbar">
      <div class="oi-map-tabs">
        {table_tabs}
      </div>
      <div class="oi-map-hint">Таблица Менделеева • Esc — закрыть</div>
    </div>

    <div class="oi-map-viewport" data-oi-table-viewport>
      {table_imgs}
    </div>
  </div>
</div>
""".strip()

    return f"""
{CSS}
<button class="oi-map-btn" type="button" data-oi-map-btn>🗺️ Карта</button>
{table_btn}

<div class="oi-map-backdrop" aria-hidden="true" data-oi-map-backdrop>
  <div class="oi-map-modal" role="dialog" aria-modal="true" aria-label="Карта">
    <button class="oi-map-close" type="button" aria-label="Закрыть" data-oi-map-close>×</button>

    <div class="oi-map-toolbar">
      <div class="oi-map-tabs">
        {map_tabs}
      </div>
      <div class="oi-map-hint">Колёсико/трекпад — зум • Esc — закрыть</div>
    </div>

    <div class="oi-map-viewport" data-oi-map-viewport>
      {map_imgs}
    </div>
  </div>
</div>

{table_block}

{JS}
""".strip()

def strip_all_old(text: str) -> str:
    # Грубая, но надёжная чистка: убираем все наши вставки по маркерам data-oi-*
    markers = [
        '<style data-oi-map-overlay>',
        '<script data-oi-map-overlay>',
        'data-oi-map-btn',
        'data-oi-table-btn',
        'data-oi-map-backdrop',
        'data-oi-table-backdrop',
        'data-oi-map-viewport',
        'data-oi-table-viewport',
        'data-oi-map-close',
        'data-oi-table-close',
        'data-oi-map-tab',
        'data-oi-table-tab',
        'data-oi-map-img',
        'data-oi-table-img',
    ]
    if not any(m in text for m in markers):
        return text

    # Вырежем всё между <style data-oi-map-overlay> ... </script> (последний) если есть
    start = text.find('<style data-oi-map-overlay>')
    if start != -1:
        end = text.rfind('</script>')
        if end != -1 and end > start:
            end += len('</script>')
            text = text[:start] + text[end:]

    # Подчистим остатки кнопок/бекдропов, если они остались
    # (на практике обычно всё ушло уже блоком выше)
    for frag in [
        '<button class="oi-map-btn" type="button" data-oi-map-btn>🗺️ Карта</button>',
        '<button class="oi-table-btn" type="button" data-oi-table-btn>🧪 Таблица</button>',
    ]:
        text = text.replace(frag, "")

    return text

def inject_replace(path: Path, overlay_html: str) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text2 = strip_all_old(text)

    if "</body>" in text2:
        text2 = text2.replace("</body>", overlay_html + "\n</body>")
    else:
        text2 += "\n" + overlay_html + "\n"

    path.write_text(text2, encoding="utf-8")
    return "ok"

def ensure_files_exist(files: list[str]) -> bool:
    for mf in files:
        p = MAPS_ROOT / mf
        if not p.exists():
            print(f"❌ Нет файла: {p}")
            return False
    return True

def main():
    # Проверим наличие файлов
    if not ensure_files_exist(ALL_MAP_FILES):
        return
    if not ensure_files_exist(MENDELEEV_FILES):
        # не стопаем весь процесс, просто предупредим
        print("⚠️ Таблица Менделеева не будет добавлена (нет файлов mendeleev_1/2).")

    total = 0

    # 1) Предметы с картами
    for folder in SUBJECT_FOLDERS:
        subject_dir = POSTERS_ROOT / folder
        if not subject_dir.exists():
            print(f"⚠️ Нет папки предмета: {subject_dir}")
            continue

        for html_file in subject_dir.rglob("*.html"):
            total += 1
            map_srcs = [rel_web_path(html_file.parent, MAPS_ROOT / mf) for mf in ALL_MAP_FILES]
            overlay = build_overlay(map_srcs=map_srcs, include_table=False)
            inject_replace(html_file, overlay)

    # 2) Химия: карты не добавляем, только таблица
    chem_dir = POSTERS_ROOT / CHEMISTRY_FOLDER
    if chem_dir.exists() and ensure_files_exist(MENDELEEV_FILES):
        for html_file in chem_dir.rglob("*.html"):
            total += 1
            # можно оставить карты пустыми и спрятать кнопку карты — но проще: покажем только таблицу
            # Чтобы не было пустой карты — сделаем одну "заглушку" (первая таблица) как "карта" не нужна.
            # Поэтому: в химии включаем table, а карту сделаем на основе первой таблицы? Нет.
            # Лучше: в химии покажем карты 1..7 тоже, если хочешь — но ты просил только таблицу.
            # Здесь сделаем overlay с картами (как есть) + таблицей? Это мешает.
            # Поэтому сделаем: карты = 1 шт. (mendeleev_1) и переименуем кнопку "🗺️ Карта" останется.
            # Чтобы строго по запросу: оставим карту, но можно убрать кнопку карты. Уберём её.
            table_srcs = [rel_web_path(html_file.parent, MAPS_ROOT / mf) for mf in MENDELEEV_FILES]

            # overlay только для таблицы: карта-часть создадим "невидимой"
            # сделаем 1 невидимую картинку, а кнопку карты спрячем через инлайн-стиль
            map_srcs_dummy = [table_srcs[0]]

            overlay = build_overlay(map_srcs=map_srcs_dummy, include_table=True, table_srcs=table_srcs)

            # спрячем кнопку карты в химии
            overlay = overlay.replace(
                '<button class="oi-map-btn" type="button" data-oi-map-btn>🗺️ Карта</button>',
                '<button class="oi-map-btn" style="display:none" type="button" data-oi-map-btn>🗺️ Карта</button>'
            )

            inject_replace(html_file, overlay)
    else:
        print(f"⚠️ Папка химии не найдена: {chem_dir} (или нет файлов mendeleev_1/2)")

    print(f"✅ Готово. Обработано HTML файлов: {total}")

if __name__ == "__main__":
    main()
