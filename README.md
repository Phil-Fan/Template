# Template

![star](https://img.shields.io/github/stars/Phil-Fan/Template)
![issue](https://img.shields.io/github/issues/Phil-Fan/Template)
![PR welcome](https://img.shields.io/badge/PR-welcome-brightgreen)
![GitHub last commit](https://img.shields.io/github/last-commit/Phil-Fan/Template)
![GitHub repo size](https://img.shields.io/github/repo-size/Phil-Fan/Template)

这个仓库收集了一些我常用的模板，包括 LaTeX、Markdown等。

[TOC]

## Quick Start

```bash
git clone https://github.com/Phil-Fan/Template.git
cd Template
```

```bash
git submodule update --init --recursive
```

交互式选择模板：

```bash
python init.py
```

构建模板：

```bash
# 命令行选择 latex_exp + beamer
python init.py --report latex_exp --slide beamer

# 选择 markdown + reveal-md，指定路径
python init.py --report markdown_template --slide reveal-md --target ~/my_project

# 只选择 slide
python init.py --slide beamer --target ~/presentation

# 选择 PPT 模板
python init.py --slide ppt --ppt-template beamer_type.pptx --target ~/presentation
```

## 报告

- [Phil-Fan/Latex_exp](https://github.com/Phil-Fan/Latex_exp/tree/main): 是我自己魔改的 LaTeX 论文模板，支持多章节独立编译和管理。

## 展示

- [Phil-Fan/PPT](https://github.com/Phil-Fan/PPT/tree/main): 整理的我在制作 PPT 过程中的一些经验、踩过的坑、总结使用的模版等。
- [Phil-Fan/reveal-md](https://github.com/Phil-Fan/reveal-md/tree/master): reveal-md template forked from [TonyCrane/slide-template](https://github.com/TonyCrane/slide-template)。
- [qychen2001/ZJU-Beamer-Template](https://github.com/qychen2001/ZJU-Beamer-Template/tree/main): 一个更好看的浙江大学 Beamer 模板，我参与了一点点小小的贡献。

## License

本仓库内容采用 [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa] 许可。

![CC BY-NC-SA 4.0][cc-by-nc-sa-image]

所有子仓库内容采用其各自的 License 许可。

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png

## Contributing

如果你有任何问题或建议，欢迎提交 [Issue](https://github.com/Phil-Fan/Template/issues) 或 [Pull Request](https://github.com/Phil-Fan/Template/pulls)。

![star history](https://api.star-history.com/svg?repos=Phil-Fan/Template&type=Date)
