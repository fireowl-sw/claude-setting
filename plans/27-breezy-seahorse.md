# 具身智能技能学习计划

## Context

用户发现具身大模型算法实习生岗位，虽然暂时不投递，但决定将其作为学习方向，补强以下技能：
- NeRF/3DGS（3D重建）
- SMPL/SMPL-X（人体参数化建模）
- 具身智能大模型
- 机器人真机开发

## 学习目标

### 短期目标（1-2个月）
1. **NeRF/3DGS基础**：理解原理，跑通demo，能简单使用
2. **SMPL入门**：了解人体参数化建模，能运行官方代码
3. **具身智能概念**：理解大模型+机器人的技术栈

### 中期目标（3-6个月）
1. **项目实践**：用NeRF/3DGS完成一个小项目
2. **仿真集成**：在ROS2/Gazebo中集成视觉重建模块
3. **论文复现**：复现1-2篇相关顶会论文

## 文件夹组织建议

### 方案A：在Resume目录下创建学习子目录
```
Resume/
├── Profile-CN.md
├── Profile-EN.md
├── Achievement Log/
├── Job Search/
├── Tailored/
└── Learning/                    # 新增：学习笔记
    ├── Embodied-AI/             # 具身智能
    │   ├── README.md
    │   ├── NeRF/                # NeRF相关
    │   ├── 3DGS/                # 3D Gaussian Splatting
    │   ├── SMPL/                # 人体参数化建模
    │   ├── Papers/              # 论文笔记
    │   └── Projects/            # 实践项目
    └── Robotics-Real/           # 真机开发（如果有）
```

**优点**：
- 学习内容直接关联求职，方便在简历中引用
- 与Achievement Log、Job Search在同一层级，逻辑清晰

**缺点**：
- Resume文件夹会变得越来越大，不纯粹是"求职材料"

---

### 方案B：创建独立的Learning目录（推荐）
```
~/  # 用户主目录
├── Resume/                     # 保持专注求职
│   ├── Profile-CN.md
│   ├── Achievement Log/
│   └── Job Search/
│
└── Learning/                   # 新增：独立学习空间
    ├── README.md               # 学习总览
    ├── Embodied-AI/            # 具身智能
    │   ├── 00-Roadmap.md       # 学习路线图
    │   ├── NeRF/               # NeRF相关
    │   │   ├── README.md
    │   │   ├── papers/         # 论文PDF+笔记
    │   │   ├── code/           # 代码实践
    │   │   └── resources/      # 学习资源
    │   ├── 3DGS/               # 3D Gaussian Splatting
    │   ├── SMPL/               # 人体参数化建模
    │   ├── Papers/             # 顶会论文（CVPR/ICCV/CoRL）
    │   └── Projects/           # 实践项目
    │
    └── Robotics-Real/          # 真机开发（如果以后有）
        ├── Hardware/           # 硬件知识
        └── Integration/        # 系统集成
```

**优点**：
- **职责分离**：Resume专注求职，Learning专注学习
- **扩展性好**：可以添加其他学习方向（如深度学习、强化学习）
- **长期价值**：不仅为求职，也是长期技术积累

**缺点**：
- 需要在两个目录间切换（但这个缺点很弱）

---

## 推荐文件夹结构（方案B详细版）

### Learning/Embodied-AI/ 目录设计
```
Learning/Embodied-AI/
│
├── 00-Roadmap.md               # 📋 学习路线图（总览）
│   - 学习目标
│   - 时间规划
│   - 里程碑检查点
│
├── NeRF/                       # 🎯 NeRF深度优先
│   ├── README.md               # NeRF是什么、为什么学、怎么学
│   ├── papers/                 # 论文学习
│   │   ├── NeRF-original/      # 原始论文（ECCV 2021）
│   │   │   ├── paper.pdf
│   │   │   └── notes.md        # 论文笔记
│   │   ├── Instant-NGP/        # 加速版本
│   │   └── other-variants/     # 其他变体
│   ├── code/                   # 代码实践
│   │   ├── official-numpy/     # 官方代码
│   │   ├── instant-ngp/        # NVIDIA实现
│   │   └── my-experiments/     # 自己的实验
│   └── resources/              # 学习资源
│       ├── video-tutorials/    # 视频教程链接
│       ├── blogs/              # 优质博客
│       └── datasets/           # 数据集
│
├── 3DGS/                       # 🎯 3D Gaussian Splatting
│   ├── README.md
│   ├── papers/
│   │   ├── 3DGS-original/      # 原始论文（SIGGRAPH 2023）
│   │   └── gaussian-splatting/
│   ├── code/
│   │   ├── official-repo/      # 官方代码
│   │   └── my-reconstruction/  # 自己的重建项目
│   └── resources/
│
├── SMPL/                       # 🎯 人体参数化建模
│   ├── README.md               # SMPL是什么、为什么重要
│   ├── papers/
│   │   ├── SMPL-original/      # 原始论文
│   │   └── SMPL-X/             # 扩展版本
│   ├── code/
│   │   ├── smplx-official/     # 官方代码库
│   │   └── body-models/        # 人体模型数据
│   └── resources/
│
├── Embodied-LLM/               # 🤖 具身大模型
│   ├── README.md
│   ├── papers/                 # RT-1, RT-2, PaLM-E等
│   ├── code/
│   └── resources/
│
├── Projects/                   # 💼 实践项目
│   ├── project-1-nerf-scene/   # 项目1：用NeRF重建场景
│   │   ├── README.md
│   │   ├── data/
│   │   ├── code/
│   │   └── results/
│   ├── project-2-3dgs-human/   # 项目2：用3DGS重建人体
│   └── project-3-embodied-gazebo/  # 项目3：集成到Gazebo
│
└── Integration/                # 🔗 与现有技术结合
    ├── ROS2-Integration.md     # 如何与ROS2结合
    ├── Gazebo-Integration.md   # 如何与Gazebo结合
    └── Future-Resume-Points.md # 学完后如何写进简历
```

## 学习时间规划

### Month 1: NeRF基础
- Week 1-2: 理解NeRF原理，读原始论文
- Week 3-4: 跑通官方代码，重建简单场景

### Month 2: 3DGS + SMPL入门
- Week 5-6: 学习3DGS，对比NeRF
- Week 7-8: SMPL基础，运行demo

### Month 3: 项目实践
- Week 9-10: 完成NeRF/3DGS小项目
- Week 11-12: 尝试与ROS2/Gazebo集成

## 学习资源推荐

### NeRF
- **论文**：NeRF: Representing Scenes as Neural Radiance Fields (ECCV 2021)
- **代码**：官方PyTorch实现、Instant-NGP（NVIDIA）
- **教程**：YouTube上的NeRF讲解视频

### 3DGS
- **论文**：3D Gaussian Splatting for Real-Time Radiance Field Rendering (SIGGRAPH 2023)
- **代码**：官方仓库、 gaussian-splatting-reproduction
- **对比**：3DGS vs NeRF 性能对比

### SMPL
- **论文**：SMPL: A Skinned Multi-Person Linear Model
- **代码**：SMPL-X官方实现
- **工具**：VIBE, ROMP（单目图像估计SMPL参数）

### 具身智能
- **论文**：RT-1, RT-2, PaLM-E, SayCan
- **代码**：RoboTk, Open X-Embodiment
- **资源**：Stanford、MIT、Berkeley的课程

## 成果物规划

学习完成后，你将拥有：
1. **论文笔记**：3-5篇核心论文的详细笔记
2. **代码实践**：跑通的NeRF/3DGS/SMPL demo
3. **小项目**：1-2个结合ROS2/Gazebo的项目
4. **简历亮点**：可以写进简历的项目经历

## 与简历对接

学完后，可以创建：
- `Achievement Log/2026-05 具身智能-NeRF场景重建.md`
- `Achievement Log/2026-06 具身智能-3DGS人体重建.md`
- `Achievement Log/2026-07 具身智能-ROS2视觉集成.md`

然后在Job Search时，重新申请类似岗位，匹配度会从40%提升到70%+。
