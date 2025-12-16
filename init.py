#!/usr/bin/env python3
"""
模板管理脚本
支持交互式和命令行两种方式选择、复制和编译模板
"""

import os
import sys
import shutil
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# 模板配置
REPORT_TEMPLATES = {
    'latex_exp': {
        'name': 'LaTeX 论文模板',
        'path': 'latex_exp',
        'has_makefile': True,
        'makefile_path': None  # 在根目录
    },
    'markdown_template': {
        'name': 'Markdown 模板',
        'path': 'markdown_template',
        'has_makefile': False,
        'makefile_path': None
    }
}

SLIDE_TEMPLATES = {
    'beamer': {
        'name': 'Beamer LaTeX 模板',
        'path': 'beamer',
        'has_makefile': True,
        'makefile_path': None  # 在根目录
    },
    'reveal-md': {
        'name': 'reveal-md 模板',
        'path': 'reveal-md',
        'has_makefile': True,
        'makefile_path': 'slide/src'  # 在子目录
    },
    'ppt': {
        'name': 'PowerPoint 模板',
        'path': 'PPT/templates',
        'has_makefile': False,
        'makefile_path': None
    }
}

# 获取脚本所在目录（模板仓库根目录）
SCRIPT_DIR = Path(__file__).parent.absolute()


def get_default_target_path():
    """生成默认目标路径：~/Downloads/template_project_TIMESTAMP"""
    downloads_dir = Path.home() / 'Downloads'
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return downloads_dir / f'template_project_{timestamp}'


def list_ppt_templates():
    """列出可用的 PPT 模板"""
    ppt_dir = SCRIPT_DIR / 'PPT' / 'templates'
    if not ppt_dir.exists():
        return []
    
    ppt_files = [f.name for f in ppt_dir.glob('*.pptx')]
    return sorted(ppt_files)


def select_templates_interactive():
    """交互式选择模板"""
    print("\n" + "="*60)
    print("模板选择")
    print("="*60)
    
    # 选择 Report 模板
    print("\n[Report 类模板]")
    print("0. 不选择")
    for i, (key, template) in enumerate(REPORT_TEMPLATES.items(), 1):
        print(f"{i}. {template['name']} ({key})")
    
    report_choice = input("\n请选择 Report 模板 (0-{}): ".format(len(REPORT_TEMPLATES)))
    try:
        report_idx = int(report_choice)
        if report_idx == 0:
            report_template = None
        elif 1 <= report_idx <= len(REPORT_TEMPLATES):
            report_template = list(REPORT_TEMPLATES.keys())[report_idx - 1]
        else:
            print("无效选择，将不选择 Report 模板")
            report_template = None
    except ValueError:
        print("无效输入，将不选择 Report 模板")
        report_template = None
    
    # 选择 Slide 模板
    print("\n[Slide 类模板]")
    print("0. 不选择")
    for i, (key, template) in enumerate(SLIDE_TEMPLATES.items(), 1):
        print(f"{i}. {template['name']} ({key})")
    
    slide_choice = input("\n请选择 Slide 模板 (0-{}): ".format(len(SLIDE_TEMPLATES)))
    try:
        slide_idx = int(slide_choice)
        if slide_idx == 0:
            slide_template = None
            ppt_template = None
        elif 1 <= slide_idx <= len(SLIDE_TEMPLATES):
            slide_key = list(SLIDE_TEMPLATES.keys())[slide_idx - 1]
            slide_template = slide_key
            
            # 如果是 PPT 模板，需要选择具体的 .pptx 文件
            if slide_key == 'ppt':
                ppt_templates = list_ppt_templates()
                if not ppt_templates:
                    print("错误: 未找到 PPT 模板文件")
                    slide_template = None
                    ppt_template = None
                else:
                    print("\n[可用的 PPT 模板文件]")
                    for i, ppt_file in enumerate(ppt_templates, 1):
                        print(f"{i}. {ppt_file}")
                    ppt_choice = input("\n请选择 PPT 模板文件 (1-{}): ".format(len(ppt_templates)))
                    try:
                        ppt_idx = int(ppt_choice)
                        if 1 <= ppt_idx <= len(ppt_templates):
                            ppt_template = ppt_templates[ppt_idx - 1]
                        else:
                            print("无效选择")
                            slide_template = None
                            ppt_template = None
                    except ValueError:
                        print("无效输入")
                        slide_template = None
                        ppt_template = None
            else:
                ppt_template = None
        else:
            print("无效选择，将不选择 Slide 模板")
            slide_template = None
            ppt_template = None
    except ValueError:
        print("无效输入，将不选择 Slide 模板")
        slide_template = None
        ppt_template = None
    
    # 选择目标路径
    print("\n[目标路径]")
    default_path = get_default_target_path()
    print(f"默认路径: {default_path}")
    target_input = input("请输入目标路径（直接回车使用默认路径）: ").strip()
    
    if target_input:
        target_path = Path(target_input).expanduser().resolve()
    else:
        target_path = default_path
    
    return report_template, slide_template, ppt_template, target_path


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='模板管理脚本 - 选择、复制和编译模板',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        示例:
        # 交互式选择
        python init.py

        # 命令行选择 latex_exp + beamer
        python init.py --report latex_exp --slide beamer

        # 选择 markdown + reveal-md，指定路径
        python init.py --report markdown_template --slide reveal-md --target ~/my_project

        # 只选择 slide
        python init.py --slide beamer --target ~/presentation

        # 选择 PPT 模板
        python init.py --slide ppt --ppt-template beamer_type.pptx --target ~/presentation
        """
    )
    
    parser.add_argument(
        '--report',
        choices=list(REPORT_TEMPLATES.keys()),
        help='选择 Report 模板'
    )
    
    parser.add_argument(
        '--slide',
        choices=list(SLIDE_TEMPLATES.keys()),
        help='选择 Slide 模板'
    )
    
    parser.add_argument(
        '--ppt-template',
        help='PPT 模板文件名（当 --slide ppt 时必需）'
    )
    
    parser.add_argument(
        '--target',
        help='目标路径（默认: ~/Downloads/template_project_TIMESTAMP）'
    )
    
    return parser.parse_args()


def copy_template(template_key, template_info, target_path, template_type=None, is_ppt=False, ppt_filename=None):
    """复制模板到目标路径
    
    Args:
        template_key: 模板键名
        template_info: 模板信息字典
        target_path: 目标路径
        template_type: 模板类型 ('report' 或 'slide')
        is_ppt: 是否为 PPT 模板
        ppt_filename: PPT 文件名
    """
    source_path = SCRIPT_DIR / template_info['path']
    
    if not source_path.exists():
        print(f"错误: 模板路径不存在: {source_path}")
        return False
    
    if is_ppt and ppt_filename:
        # PPT 模板：只复制单个文件到 slide 文件夹
        source_file = source_path / ppt_filename
        if not source_file.exists():
            print(f"错误: PPT 模板文件不存在: {source_file}")
            return False
        
        slide_dir = target_path / 'slide'
        slide_dir.mkdir(parents=True, exist_ok=True)
        target_file = slide_dir / ppt_filename
        shutil.copy2(source_file, target_file)
        print(f"✓ 已复制 PPT 模板: {ppt_filename} -> {slide_dir}")
        return True
    else:
        # 其他模板：根据类型复制到 report 或 slide 文件夹
        if template_type == 'report':
            target_template_path = target_path / 'report'
        elif template_type == 'slide':
            target_template_path = target_path / 'slide'
        else:
            # 如果没有指定类型，使用原来的方式（向后兼容）
            target_template_path = target_path / template_key
        
        if target_template_path.exists():
            response = input(f"目标路径已存在: {target_template_path}\n是否覆盖? (y/N): ").strip().lower()
            if response != 'y':
                print("已取消复制")
                return False
            shutil.rmtree(target_template_path)
        
        shutil.copytree(source_path, target_template_path, ignore=shutil.ignore_patterns(
            '*.aux', '*.log', '*.out', '*.toc', '*.synctex.gz', '*.bbl', '*.blg',
            '*.fls', '*.fdb_latexmk', '*.nav', '*.snm', '*.vrb', '*.pdf',
            '*.aux', 'site', '__pycache__', '*.pyc', '.git'
        ))
        print(f"✓ 已复制模板: {template_key} -> {target_template_path}")
        return True


def find_makefile(base_path):
    """查找 Makefile 位置"""
    # 首先检查根目录
    makefile_path = base_path / 'Makefile'
    if makefile_path.exists():
        return base_path
    
    # 检查常见子目录
    common_subdirs = ['slide/src', 'src', 'slide']
    for subdir in common_subdirs:
        subdir_path = base_path / subdir
        makefile_path = subdir_path / 'Makefile'
        if makefile_path.exists():
            return subdir_path
    
    # 递归查找（最多3层）
    for root, dirs, files in os.walk(base_path):
        depth = root[len(str(base_path)):].count(os.sep)
        if depth > 3:
            continue
        if 'Makefile' in files:
            return Path(root)
    
    return None


def compile_template(template_key, template_info, target_path, template_type=None):
    """编译模板（使用 Makefile）
    
    Args:
        template_key: 模板键名
        template_info: 模板信息字典
        target_path: 目标路径
        template_type: 模板类型 ('report' 或 'slide')
    """
    if not template_info['has_makefile']:
        print(f"模板 {template_key} 不需要编译")
        return True
    
    # 确定模板在目标路径中的位置
    if template_key == 'ppt':
        # PPT 模板不需要编译
        return True
    
    # 根据类型确定模板路径
    if template_type == 'report':
        template_target_path = target_path / 'report'
    elif template_type == 'slide':
        template_target_path = target_path / 'slide'
    else:
        # 向后兼容：使用原来的方式
        template_target_path = target_path / template_key
    
    # 查找 Makefile
    makefile_dir = find_makefile(template_target_path)
    
    if makefile_dir is None:
        print(f"警告: 未找到 {template_key} 的 Makefile，跳过编译")
        return False
    
    print(f"找到 Makefile 在: {makefile_dir}")
    print(f"正在编译 {template_key}...")
    
    try:
        # 运行 make
        result = subprocess.run(
            ['make'],
            cwd=makefile_dir,
            check=False,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ {template_key} 编译成功")
            return True
        else:
            print(f"✗ {template_key} 编译失败")
            if result.stdout:
                print("标准输出:")
                print(result.stdout)
            if result.stderr:
                print("错误输出:")
                print(result.stderr)
            return False
    except FileNotFoundError:
        print("错误: 未找到 make 命令，请确保已安装 make")
        return False
    except Exception as e:
        print(f"编译时发生错误: {e}")
        return False


def main():
    """主函数"""
    # 检查是否在模板仓库根目录
    if not (SCRIPT_DIR / 'latex_exp').exists():
        print("错误: 请在模板仓库根目录运行此脚本")
        sys.exit(1)
    
    # 解析参数或使用交互式选择
    if len(sys.argv) > 1:
        # 命令行模式
        args = parse_arguments()
        report_template = args.report
        slide_template = args.slide
        ppt_template = args.ppt_template
        
        if args.target:
            target_path = Path(args.target).expanduser().resolve()
        else:
            target_path = get_default_target_path()
        
        # 验证 PPT 模板参数
        if slide_template == 'ppt' and not ppt_template:
            ppt_templates = list_ppt_templates()
            if not ppt_templates:
                print("错误: 未找到 PPT 模板文件")
                sys.exit(1)
            print("错误: 使用 --slide ppt 时必须指定 --ppt-template")
            print(f"可用的 PPT 模板: {', '.join(ppt_templates)}")
            sys.exit(1)
    else:
        # 交互式模式
        report_template, slide_template, ppt_template, target_path = select_templates_interactive()
    
    # 验证至少选择了一个模板
    if not report_template and not slide_template:
        print("错误: 至少需要选择一个模板")
        sys.exit(1)
    
    # 显示选择结果
    print("\n" + "="*60)
    print("选择的模板:")
    print("="*60)
    if report_template:
        print(f"  Report: {REPORT_TEMPLATES[report_template]['name']}")
    if slide_template:
        if slide_template == 'ppt':
            print(f"  Slide: {SLIDE_TEMPLATES[slide_template]['name']} ({ppt_template})")
        else:
            print(f"  Slide: {SLIDE_TEMPLATES[slide_template]['name']}")
    print(f"  目标路径: {target_path}")
    print("="*60 + "\n")
    
    # 确认
    if len(sys.argv) == 1:  # 只在交互式模式下确认
        confirm = input("确认开始复制和编译? (Y/n): ").strip().lower()
        if confirm == 'n':
            print("已取消")
            sys.exit(0)
    
    # 创建目标目录
    target_path.mkdir(parents=True, exist_ok=True)
    
    # 复制模板
    success = True
    
    if report_template:
        template_info = REPORT_TEMPLATES[report_template]
        if not copy_template(report_template, template_info, target_path, template_type='report'):
            success = False
    
    if slide_template:
        template_info = SLIDE_TEMPLATES[slide_template]
        is_ppt = (slide_template == 'ppt')
        if not copy_template(slide_template, template_info, target_path, template_type='slide', is_ppt=is_ppt, ppt_filename=ppt_template):
            success = False
    
    if not success:
        print("\n复制过程中出现错误，请检查上述信息")
        sys.exit(1)
    
    # 编译模板
    print("\n" + "="*60)
    print("开始编译")
    print("="*60 + "\n")
    
    compile_success = True
    
    if report_template:
        template_info = REPORT_TEMPLATES[report_template]
        if not compile_template(report_template, template_info, target_path, template_type='report'):
            compile_success = False
    
    if slide_template and slide_template != 'ppt':
        template_info = SLIDE_TEMPLATES[slide_template]
        if not compile_template(slide_template, template_info, target_path, template_type='slide'):
            compile_success = False
    
    # 总结
    print("\n" + "="*60)
    print("完成")
    print("="*60)
    print(f"模板已复制到: {target_path}")
    if compile_success:
        print("所有模板编译成功！")
    else:
        print("部分模板编译失败，请检查上述错误信息")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()

