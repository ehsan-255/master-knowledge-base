#!/usr/bin/env python3
"""
Test Script for Migration Scripts

This script validates that all migration scripts can be imported and basic
functionality works correctly before attempting the actual migration.

Author: Automated Migration System
Generated: 2025-01-27
"""

import sys
import logging
from pathlib import Path

def setup_test_logging():
    """Setup logging for tests."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)

def test_imports():
    """Test that all migration scripts can be imported."""
    logger = setup_test_logging()
    logger.info("Testing script imports...")
    
    try:
        # Test main controller import
        from migrate_master_kb_to_root import MigrationController
        logger.info("✅ migrate_master_kb_to_root imported successfully")
        
        # Test path reference updater import
        from update_path_references import PathReferenceUpdater
        logger.info("✅ update_path_references imported successfully")
        
        # Test file structure migrator import
        from migrate_file_structure import FileStructureMigrator
        logger.info("✅ migrate_file_structure imported successfully")
        
        # Test validation suite import
        from validate_migration import MigrationValidator
        logger.info("✅ validate_migration imported successfully")
        
        # Test rollback manager import
        from rollback_migration import RollbackManager
        logger.info("✅ rollback_migration imported successfully")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during import: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of migration scripts."""
    logger = setup_test_logging()
    logger.info("Testing basic functionality...")
    
    try:
        # Get repository root (3 levels up from this script)
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent
        
        if not (repo_root / "master-knowledge-base").exists():
            logger.error("❌ Repository structure not found")
            return False
        
        logger.info(f"Repository root: {repo_root}")
        
        # Test MigrationController initialization
        from migrate_master_kb_to_root import MigrationController
        controller = MigrationController(repo_root, dry_run=True)
        logger.info("✅ MigrationController initialized successfully")
        
        # Test PathReferenceUpdater initialization
        from update_path_references import PathReferenceUpdater
        updater = PathReferenceUpdater(repo_root, True, logger)
        logger.info("✅ PathReferenceUpdater initialized successfully")
        
        # Test FileStructureMigrator initialization
        from migrate_file_structure import FileStructureMigrator
        migrator = FileStructureMigrator(repo_root, True, logger)
        logger.info("✅ FileStructureMigrator initialized successfully")
        
        # Test MigrationValidator initialization
        from validate_migration import MigrationValidator
        validator = MigrationValidator(repo_root, logger)
        logger.info("✅ MigrationValidator initialized successfully")
        
        # Test RollbackManager initialization
        from rollback_migration import RollbackManager
        rollback_mgr = RollbackManager(repo_root, logger)
        logger.info("✅ RollbackManager initialized successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Functionality test failed: {e}")
        return False

def test_file_discovery():
    """Test file discovery functionality."""
    logger = setup_test_logging()
    logger.info("Testing file discovery...")
    
    try:
        # Get repository root
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent
        
        # Test path reference updater file discovery
        from update_path_references import PathReferenceUpdater
        updater = PathReferenceUpdater(repo_root, True, logger)
        files = updater.get_files_to_process()
        
        logger.info(f"✅ Found {len(files)} files to process")
        
        if len(files) < 50:
            logger.warning("⚠️  Fewer files found than expected")
        
        # Test validation file discovery
        from validate_migration import MigrationValidator
        validator = MigrationValidator(repo_root, logger)
        text_files = validator.get_text_files()
        
        logger.info(f"✅ Found {len(text_files)} text files for validation")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ File discovery test failed: {e}")
        return False

def test_conflict_detection():
    """Test conflict detection functionality."""
    logger = setup_test_logging()
    logger.info("Testing conflict detection...")
    
    try:
        # Get repository root
        script_dir = Path(__file__).parent
        repo_root = script_dir.parent.parent
        
        # Test file structure migrator conflict detection
        from migrate_file_structure import FileStructureMigrator
        migrator = FileStructureMigrator(repo_root, True, logger)
        conflicts = migrator.check_conflicts()
        
        if conflicts:
            logger.warning(f"⚠️  {len(conflicts)} conflicts detected:")
            for conflict in conflicts:
                logger.warning(f"    - {conflict}")
        else:
            logger.info("✅ No conflicts detected")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Conflict detection test failed: {e}")
        return False

def run_all_tests():
    """Run all validation tests."""
    logger = setup_test_logging()
    logger.info("=" * 60)
    logger.info("MIGRATION SCRIPTS VALIDATION TEST SUITE")
    logger.info("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality Tests", test_basic_functionality),
        ("File Discovery Tests", test_file_discovery),
        ("Conflict Detection Tests", test_conflict_detection)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n🔄 Running: {test_name}")
        
        try:
            if test_func():
                logger.info(f"✅ {test_name} PASSED")
                passed += 1
            else:
                logger.error(f"❌ {test_name} FAILED")
                failed += 1
        except Exception as e:
            logger.error(f"❌ {test_name} FAILED with exception: {e}")
            failed += 1
    
    # Summary
    logger.info("=" * 60)
    logger.info("TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Tests Passed: {passed}")
    logger.info(f"Tests Failed: {failed}")
    logger.info(f"Total Tests: {passed + failed}")
    
    if failed == 0:
        logger.info("🎉 ALL TESTS PASSED - Migration scripts are ready for use")
        logger.info("📋 You can now proceed with: python migrate_master_kb_to_root.py --dry-run")
        return True
    else:
        logger.error("❌ SOME TESTS FAILED - Fix issues before running migration")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 