#!/usr/bin/env python3
"""
Migration script to refactor automation-testing-playground to comply with 
Personal GitHub Repository Rules.

This script:
1. Moves helpers/, pages/, config/, performance/, security/ to src/automation_testing_playground/
2. Updates all imports throughout the codebase
3. Moves HTML reports to artifacts/reports/
4. Creates __init__.py files where needed
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Tuple

# Directories to move from root to src/automation_testing_playground/
DIRECTORIES_TO_MOVE = [
    'helpers',
    'pages',
    'config',
    'performance',
    'security'
]

# HTML report files to move
HTML_REPORTS = [
    'cart_report.html',
    'cart_removal_report.html',
    'dashboard.html',
    'last_report.html'
]

# Import patterns to update
IMPORT_PATTERNS = [
    (r'from helpers\.', 'from automation_testing_playground.helpers.'),
    (r'from pages\.', 'from automation_testing_playground.pages.'),
    (r'from config\.', 'from automation_testing_playground.config.'),
    (r'from performance\.', 'from automation_testing_playground.performance.'),
    (r'from security\.', 'from automation_testing_playground.security.'),
    (r'import helpers\.', 'import automation_testing_playground.helpers.'),
    (r'import pages\.', 'import automation_testing_playground.pages.'),
    (r'import config\.', 'import automation_testing_playground.config.'),
    (r'import performance\.', 'import automation_testing_playground.performance.'),
    (r'import security\.', 'import automation_testing_playground.security.'),
]

# Path patterns to update in run_tests.py and other scripts
PATH_PATTERNS = [
    (r'"performance/', '"src/automation_testing_playground/performance/'),
    (r"'performance/", "'src/automation_testing_playground/performance/"),
]


def create_directory_structure():
    """Create the target directory structure"""
    print("📁 Creating directory structure...")
    
    # Create src/automation_testing_playground/
    target_dir = Path('src/automation_testing_playground')
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_file = target_dir / '__init__.py'
    if not init_file.exists():
        init_file.write_text('# Automation Testing Playground Package\n')
        print(f"  ✅ Created {init_file}")
    
    # Create artifacts/reports/
    artifacts_dir = Path('artifacts/reports')
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ Created {artifacts_dir}")
    
    print("  ✅ Directory structure created\n")


def move_directories():
    """Move directories from root to src/automation_testing_playground/"""
    print("📦 Moving directories...")
    
    target_base = Path('src/automation_testing_playground')
    
    for dir_name in DIRECTORIES_TO_MOVE:
        source = Path(dir_name)
        target = target_base / dir_name
        
        if source.exists() and source.is_dir():
            if target.exists():
                print(f"  ⚠️  {target} already exists, skipping...")
                continue
            
            # Move the directory
            shutil.move(str(source), str(target))
            print(f"  ✅ Moved {source} → {target}")
            
            # Create __init__.py if it doesn't exist
            init_file = target / '__init__.py'
            if not init_file.exists():
                init_file.write_text(f'# {dir_name.title()} module\n')
        else:
            print(f"  ⚠️  {source} not found, skipping...")
    
    print()


def move_html_reports():
    """Move HTML reports to artifacts/reports/"""
    print("📄 Moving HTML reports...")
    
    artifacts_dir = Path('artifacts/reports')
    
    for html_file in HTML_REPORTS:
        source = Path(html_file)
        target = artifacts_dir / html_file
        
        if source.exists() and source.is_file():
            if target.exists():
                print(f"  ⚠️  {target} already exists, skipping...")
                continue
            
            shutil.move(str(source), str(target))
            print(f"  ✅ Moved {source} → {target}")
        else:
            print(f"  ⚠️  {source} not found, skipping...")
    
    print()


def update_imports_in_file(file_path: Path) -> bool:
    """Update imports in a single file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Update import patterns
        for pattern, replacement in IMPORT_PATTERNS:
            content = re.sub(pattern, replacement, content)
        
        # Update path patterns
        for pattern, replacement in PATH_PATTERNS:
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"  ❌ Error updating {file_path}: {e}")
        return False


def update_imports():
    """Update imports throughout the codebase"""
    print("🔧 Updating imports...")
    
    updated_count = 0
    
    # Update Python files in src/
    for py_file in Path('src').rglob('*.py'):
        if update_imports_in_file(py_file):
            updated_count += 1
            print(f"  ✅ Updated {py_file}")
    
    # Update Python files in tests/
    for py_file in Path('tests').rglob('*.py'):
        if update_imports_in_file(py_file):
            updated_count += 1
            print(f"  ✅ Updated {py_file}")
    
    # Update scripts/
    for py_file in Path('scripts').rglob('*.py'):
        if update_imports_in_file(py_file):
            updated_count += 1
            print(f"  ✅ Updated {py_file}")
    
    print(f"  ✅ Updated {updated_count} files\n")


def verify_structure():
    """Verify the final structure"""
    print("✅ Verifying structure...")
    
    checks = [
        ('src/automation_testing_playground/', Path('src/automation_testing_playground').exists()),
        ('artifacts/reports/', Path('artifacts/reports').exists()),
        ('scripts/', Path('scripts').exists()),
    ]
    
    for name, exists in checks:
        status = "✅" if exists else "❌"
        print(f"  {status} {name}")
    
    # Check that directories were moved
    target_base = Path('src/automation_testing_playground')
    for dir_name in DIRECTORIES_TO_MOVE:
        target = target_base / dir_name
        source = Path(dir_name)
        if target.exists():
            print(f"  ✅ {dir_name} moved correctly")
        elif source.exists():
            print(f"  ⚠️  {dir_name} still in root (needs manual move)")
        else:
            print(f"  ⚠️  {dir_name} not found")
    
    print()


def main():
    """Main migration function"""
    print("🚀 Starting repository refactoring...\n")
    
    try:
        create_directory_structure()
        move_directories()
        move_html_reports()
        update_imports()
        verify_structure()
        
        print("✅ Migration complete!")
        print("\n📝 Next steps:")
        print("  1. Review the changes")
        print("  2. Run tests to ensure everything works")
        print("  3. Update README.md structure section")
        print("  4. Commit the changes")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise


if __name__ == '__main__':
    main()
