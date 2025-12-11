// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: ['getting-started/setup-and-installation'],
    },
    {
      type: 'category',
      label: 'Physical AI Concepts',
      items: ['physical-ai/fundamentals'],
    },
    {
      type: 'category',
      label: 'ROS 2 Fundamentals',
      items: ['ros2/basics'],
    },
    {
      type: 'category',
      label: 'Gazebo Simulation',
      items: ['gazebo/introduction'],
    },
    {
      type: 'category',
      label: 'Unity Visualization',
      items: ['unity/getting-started'],
    },
    {
      type: 'category',
      label: 'NVIDIA Isaac Platform',
      items: ['nvidia-isaac/introduction'],
    },
    {
      type: 'category',
      label: 'Vision-Language-Action Systems',
      items: ['vla/systems'],
    },
    {
      type: 'category',
      label: 'Humanoid Robot Kinematics',
      items: ['kinematics/introduction'],
    },
    {
      type: 'category',
      label: 'Conversational Robotics',
      items: ['conversational-robotics/introduction'],
    },
    {
      type: 'category',
      label: 'Advanced Projects',
      items: ['advanced-projects/project-examples'],
    },
  ],
};

export default sidebars;