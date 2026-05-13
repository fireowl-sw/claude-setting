const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, ImageRun, WidthType } = require('docx');

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 24 } // 12pt default
      }
    },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 }
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 28, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 }
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
      }
    },
    children: [
      // Title
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("1 LiDAR and Semantic LiDAR")]
      }),

      // Section 1.1
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.1 Introduction")]
      }),

      new Paragraph({
        children: [new TextRun("LiDAR is a core sensor for environmental perception in autonomous driving. It can acquire high-precision 3D point clouds to construct scenes and detect obstacles. Semantic LiDAR adds labels to the point cloud, allowing us to understand the semantic information corresponding to the objects represented by the point cloud. In this chapter, we build a LiDAR simulation environment using the Carla simulator and ROS 2, and implement the simulation of point cloud mapping and visualization for LiDAR.")]
      }),

      // Section 1.2
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.2 ROS2 LiDAR Mapping Node")]
      }),

      new Paragraph({
        children: [new TextRun("To achieve the mapping and visualization of LiDAR point clouds, I have developed a custom ROS2 package named carla_lidar_mapping_ros2.")]
      }),

      new Paragraph({
        children: [new TextRun("The project structure is shown below.")]
      }),

      // Code block
      new Paragraph({
        children: [new TextRun({
          text: "a_carla_sim/\n├── src/\n│   ├── carla_ros_bridge/        # CARLA-ROS Bridge\n│   ├── carla_lidar_mapping_ros2/ # Custom Mapping Package\n│   │   ├── src/                  # Node Implementation\n│   │   ├── launch/               # Launch Files\n│   │   ├── config/               # Configuration Files\n│   │   ├── maps/                 # Generated Point Cloud Maps\n│   │   └── rviz/                 # Visualization Configs\n│   └── pcl_recorder/             # Point Cloud Recorder\n└── run_core.sh                   # Simulation Startup Script",
          font: "Consolas",
          size: 20,
          shading: "F5F5F5"
        })]
      }),

      new Paragraph({
        children: [new TextRun("The carla_lidar_mapping_ros2 package converts the LiDAR point cloud data in the local coordinate system obtained from the Carla simulator to the global map coordinate system, accumulates multi-frame point clouds at time intervals to construct a complete environmental map, and then achieves real-time visualization through RViz, thus fulfilling the goal of LiDAR point cloud mapping.")]
      }),

      new Paragraph({
        children: [new TextRun("The node topic subscription and publishing in ROS2 are shown in the figure below:")]
      }),

      // Mermaid diagram reference
      new Paragraph({
        children: [new TextRun({
          text: "[ROS2 Topic Flow Graph]\nCARLA Simulator → /carla/vehicle/lidar → carla_ros_bridge → /carla/vehicle/lidar/sensor_type/point_cloud → carla_lidar_mapping_ros2 → /map/point_cloud → RViz",
          font: "Consolas",
          size: 20,
          italics: true
        })]
      }),

      // Section 1.3
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.3 Point Cloud Map vs Simulated Map")]
      }),

      new Paragraph({
        children: [new TextRun("By launching the autonomous driving package in carla_ros_bridge and letting the vehicle drive autonomously for a period of time, a point cloud map generated from the simulation map can be obtained.")]
      }),

      new Paragraph({
        children: [new TextRun({
          text: "[Image: Point cloud map comparison - showing buildings, roads, and infrastructure]",
          italics: true,
          color: "666666"
        })]
      }),

      new Paragraph({
        children: [new TextRun("As can be seen from the figure, the generated point cloud map accurately reproduces the buildings, roads, and other infrastructure in the simulation environment.The LiDAR point cloud reflects the three-dimensional spatial information of the simulation environment collected by the LiDAR sensor at different positions and angles.After coordinate transformation by the carla_lidar_mapping_ros2 package, the LiDAR point cloud is converted into a point cloud map under the map coordinate system, which corresponds to the left image.")]
      }),

      // Section 1.4
      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.4 Semantic LiDAR Demonstration")]
      }),

      new Paragraph({
        children: [new TextRun("Semantic LiDAR adds semantic information on the basis of LiDAR. By marking different colors, we can distinguish different objects. The figure below shows the visualization of LiDAR point clouds in the simulation.")]
      }),

      new Paragraph({
        children: [new TextRun({
          text: "[Image: Standard LiDAR point cloud visualization]",
          italics: true,
          color: "666666"
        })]
      }),

      new Paragraph({
        children: [new TextRun("Through deep learning training, semantic information is added to each point in the point cloud, and we can use different colors to distinguish objects in the simulation.")]
      }),

      new Paragraph({
        children: [new TextRun("The figure below shows the visualization of the Semantic LiDAR point cloud in the simulation.")]
      }),

      new Paragraph({
        children: [new TextRun({
          text: "[Image: Semantic LiDAR point cloud - green=trees, purple=curbs, orange=buildings, yellow=fences]",
          italics: true,
          color: "666666"
        })]
      }),

      new Paragraph({
        children: [new TextRun("As can be seen from the figure, green represents trees, purple represents curbs, orange represents buildings, and yellow represents fences. With these semantic labels, we can implement functions such as intelligent obstacle avoidance and hierarchical semantic high-definition maps.")]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Weekly_Presentation_Report_Part1.docx", buffer);
  console.log("Document created successfully!");
});
