# TimeTracker Alkalmazás

Ez egy asztali alkalmazás feladatok idejének követésére, amelyet Pythonnal fejlesztettek. Egy helyi FastAPI backend API-t használ az adatok kezelésére és egy PySide6 grafikus felhasználói felületet (GUI) a felhasználói interakciókhoz.

## Architektúra

Az alkalmazás két fő részből áll:

1.  **Backend:** Egy FastAPI alapú webes API, amely a `uvicorn` szerveren fut. Felelős a feladatok adatainak (létrehozás, olvasás, frissítés, törlés - CRUD), az időmérés állapotának kezeléséért és az adatok perzisztens tárolásáért.
2.  **Frontend:** Egy PySide6 alapú asztali GUI alkalmazás. Lehetővé teszi a felhasználók számára, hogy megtekintsék, hozzáadjanak, szerkesszenek, töröljenek feladatokat, valamint elindítsák és leállítsák az időmérést az egyes feladatokhoz. Kommunikál a Backend API-val HTTP kéréseken keresztül.

Az alkalmazás indítását a [start_app.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/start_app.py:0:0-0:0) szkript végzi, amely először elindítja a Backendet egy háttérszálon, majd elindítja a Frontend GUI-t a fő szálon.

## Fő Komponensek és Adatfolyam

*   **Indítás ([start_app.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/start_app.py:0:0-0:0)):**
    *   Elindítja a [run_backend](cci:1://file:///c:/GIT/TimeMeter/task-tracker/start_app.py:10:0-12:63) függvényt (Uvicorn szerver a `backend.main:app`-al) egy külön `Thread`-ben.
    *   Létrehozza a `QApplication`-t és a [MainWindow](cci:2://file:///c:/GIT/TimeMeter/task-tracker/frontend/components/main_window.py:19:0-174:27)-t (`frontend.components.main_window.MainWindow`).
*   **Frontend (`frontend/`):**
    *   [MainWindow](cci:2://file:///c:/GIT/TimeMeter/task-tracker/frontend/components/main_window.py:19:0-174:27): A fő alkalmazásablak. Tartalmazza a feladatlistát (`QListWidget`), gombokat a műveletekhez (új, törlés, frissítés, logok), és egy tálcaikont (`QSystemTrayIcon`).
    *   `APIClient` (`frontend.services.api_client.APIClient`): Osztály, amely becsomagolja a Backend API hívásokat (valószínűleg a `requests` könyvtárat használva). A [MainWindow](cci:2://file:///c:/GIT/TimeMeter/task-tracker/frontend/components/main_window.py:19:0-174:27) és más komponensek ezt használják a backenddel való kommunikációra.
    *   `TaskTimerManager` (`frontend.core.task_timer_manager.TaskTimerManager`): Kezeli a frontend oldali időzítési logikát (pl. egy aktív feladat időtartamának kijelzése).
    *   `FloatingControlWindow`: Egy "lebegő" ablak, amely gyors hozzáférést biztosít az időmérés indításához/leállításához és az aktuális feladat kiválasztásához. Kommunikál a [MainWindow](cci:2://file:///c:/GIT/TimeMeter/task-tracker/frontend/components/main_window.py:19:0-174:27)-val és az `APIClient`-tel.
    *   `WindowTitleWatcher`: Figyeli az aktív ablak címét, és ha az "Ablak alapú ajánlás" be van kapcsolva, javaslatot tehet releváns feladat indítására a `FloatingControlWindow`-n keresztül (a backend `/suggest` végpontját használva).
    *   Dialógusok (`NewTaskDialog`, `EditTaskDialog`): Felugró ablakok új feladatok létrehozásához és meglévők szerkesztéséhez. Az `APIClient`-et használják a backend műveletek végrehajtásához.
    *   `LogWindow`: Ablak a backend log fájl (`backend.log`) tartalmának megjelenítésére.
*   **Backend ([backend/](cci:1://file:///c:/GIT/TimeMeter/task-tracker/start_app.py:10:0-12:63)):**
    *   `main.py`: Létrehozza a `FastAPI` alkalmazást ([app](cci:1://file:///c:/GIT/TimeMeter/task-tracker/frontend/components/main_window.py:171:4-174:27)), csatolja a `tasks.router`-t a `/tasks` útvonal alá.
    *   `api/tasks.py`: Definiálja az `APIRouter`-t és az összes `/tasks/...` végpontot.
        *   Fogadja a HTTP kéréseket a Frontentől.
        *   Használja a [schemas.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:0:0-0:0)-ben definiált Pydantic modelleket ([TaskSchema](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:4:0-8:38), [Task](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:10:0-19:101), [TaskTemplateSchema](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:23:0-27:38)) az adatok validálására/szerializálására.
        *   Meghívja a [get_shared_task_manager()](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:122:0-126:33)-t, hogy hozzáférjen a [TaskManager](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:4:0-117:19) példányhoz.
        *   Meghívja a [TaskManager](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:4:0-117:19) metódusait (pl. [add_task](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:29:4-48:24), [get_all_tasks](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:8:4-17:20), [start_task](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:90:4-102:19)).
    *   [core/task_manager.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:0:0-0:0):
        *   [TaskManager](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:4:0-117:19): Singleton osztály, amely az üzleti logikát tartalmazza.
        *   Inicializáláskor létrehoz egy [Storage](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:5:0-31:31) példányt.
        *   Metódusai kezelik a feladatok létrehozását, módosítását, törlését, állapotváltozásait (indítás/leállítás), ID és belső [title](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/core/task_manager.py:24:4-27:37) generálását, valamint a feladatokhoz tartozó `logs` lista frissítését.
        *   Minden adatmanipuláció előtt betölti (`storage.load_tasks`), majd a módosítás után elmenti (`storage.save_tasks`) az adatokat a [Storage](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:5:0-31:31)-on keresztül.
        *   Meghívja a `storage.check_and_archive`-ot mentés után.
    *   [data/storage.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:0:0-0:0):
        *   [Storage](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:5:0-31:31): Osztály, amely a perzisztens tárolást kezeli.
        *   Az adatokat a `backend/data/tasks.json` fájlban tárolja.
        *   [load_tasks](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:11:4-18:25): Beolvassa a JSON fájlt.
        *   [save_tasks](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:20:4-22:64): Felülírja a JSON fájlt a megadott adatokkal.
        *   [check_and_archive](cci:1://file:///c:/GIT/TimeMeter/task-tracker/backend/data/storage.py:24:4-31:31): Ha a fájl túl nagy vagy túl sok feladatot tartalmaz, átmozgatja a `backend/data/archive/` mappába egy időbélyeggel ellátott névvel, és új, üres `tasks.json`-t hoz létre.
    *   [api/schemas.py](cci:7://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:0:0-0:0): Pydantic modellek ([TaskSchema](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:4:0-8:38), [Task](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:10:0-19:101), [TaskTemplateSchema](cci:2://file:///c:/GIT/TimeMeter/task-tracker/backend/api/schemas.py:23:0-27:38)) az API adatszerkezetek definíciójához és validációjához.

## Adattárolás

A feladatok adatai egy JSON fájlban (`backend/data/tasks.json`) tárolódnak. A fájl automatikusan archiválódik (`backend/data/archive/`), ha elér egy bizonyos méretet vagy feladatszámot, hogy az aktív fájl kezelhető maradjon.

## Függőségek

*   **Backend:** FastAPI, Uvicorn, Pydantic
*   **Frontend:** PySide6
*   **Adatkezelés:** (beépített `json`)
*   **Kommunikáció:** (valószínűleg `requests` a frontend oldalon)
*   **Egyéb:** `openpyxl` (Excel export/import lehetőség?), `pytest` (tesztelés)

Lásd a `requirements.txt` fájlt a pontos listáért.

## Indítás

1.  Telepítsd a függőségeket: `pip install -r requirements.txt`
2.  Futtasd az alkalmazást: `python start_app.py`
