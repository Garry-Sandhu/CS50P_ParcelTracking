import pytest
import project

def test_main_dashboard(monkeypatch):
    # Simulate selecting "Dashboard"
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "show_dashboard", lambda: "dashboard")
    monkeypatch.setattr(project, "create_package", lambda: "created")
    monkeypatch.setattr(project, "update_package_status", lambda: "updated")
    monkeypatch.setattr(project, "delete_package_by_id", lambda: "deleted")
    monkeypatch.setattr(project, "track_package_by_id", lambda: "tracked")
    monkeypatch.setattr(project, "view_status_history", lambda: "history")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "Dashboard"})())
    assert project.main() is None  # just runs without error

def test_main_create_package(monkeypatch):
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "create_package", lambda: "created")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "Create Package"})())
    assert project.main() is None

def test_main_update_status(monkeypatch):
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "update_package_status", lambda: "updated")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "Update Status"})())
    assert project.main() is None

def test_main_delete_package(monkeypatch):
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "delete_package_by_id", lambda: "deleted")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "Delete Package"})())
    assert project.main() is None

def test_main_track_package(monkeypatch):
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "track_package_by_id", lambda: "tracked")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "Track Package"})())
    assert project.main() is None

def test_main_view_history(monkeypatch):
    monkeypatch.setattr(project, "init_db", lambda: None)
    monkeypatch.setattr(project, "view_status_history", lambda: "history")
    monkeypatch.setattr(project, "st", type("Dummy", (), {"radio": lambda *a, **k: "View History"})())
    assert project.main() is None

def test_show_dashboard(monkeypatch):
    import pandas as pd
    monkeypatch.setattr("project.get_status_distribution",
                        lambda: pd.DataFrame({"Status": ["Delivered"], "Count": [5]}))
    monkeypatch.setattr("project.get_recent_packages",
                        lambda: pd.DataFrame({"PackageID": [1], "Status": ["Delivered"]}))
    assert project.show_dashboard() is None
