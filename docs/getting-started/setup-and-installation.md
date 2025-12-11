---
sidebar_position: 1
---

# Setup and Installation

This guide will walk you through setting up your development environment for working with Physical AI and Humanoid Robotics. We'll cover the essential tools and frameworks you'll need throughout this textbook.

## Prerequisites

Before installing the software required for this textbook, ensure your system meets the following requirements:

- **Operating System**: Ubuntu 20.04 LTS or Windows 10/11 (with WSL2 recommended)
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 20GB of free space
- **Processor**: Multi-core processor (Intel i5/Ryzen 5 or better recommended)
- **Graphics**: GPU with CUDA support recommended for NVIDIA Isaac tools (optional but recommended)

## Installing Required Software

### 1. Development Environment Setup

#### Option A: Native Ubuntu Installation
```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install basic development tools
sudo apt install -y build-essential cmake git python3-pip wget curl gnupg lsb-release
```

#### Option B: Windows with WSL2
1. Install WSL2 with Ubuntu 20.04 distribution from Microsoft Store
2. Follow the Ubuntu installation steps inside the WSL2 terminal

### 2. ROS 2 Installation

Follow the official ROS 2 Humble Hawksbill installation guide:
```bash
# Set locale
locale-gen en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS 2 apt repository
sudo apt update && sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS 2 packages
sudo apt update
sudo apt install -y ros-humble-desktop
sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential
```

### 3. Gazebo Installation

Install Gazebo Harmonic:
```bash
# Add Gazebo repository
wget https://packages.osrfoundation.org/gazebo.gpg -O /tmp/gazebo.gpg
sudo mv /tmp/gazebo.gpg /usr/share/keyrings/
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gazebo.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Update and install
sudo apt update
sudo apt install gazebo-harmonic
```

### 4. Node.js and npm (for Docusaurus documentation)

```bash
# Install nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart your terminal or run:
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install latest LTS version of Node.js
nvm install --lts
nvm use --lts
```

### 5. Python Virtual Environment

```bash
# Install venv if not already installed
sudo apt install python3-venv

# Create a virtual environment
python3 -m venv ~/physical_ai_env
source ~/physical_ai_env/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 6. Other Useful Tools

```bash
# Install Docker (for containerized development)
sudo apt install docker.io
sudo usermod -aG docker $USER # Add user to docker group (requires logout/relogin)

# Install Visual Studio Code
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

## Verification Steps

After completing the installation, verify that the key components are working:

```bash
# Verify ROS 2 installation
source /opt/ros/humble/setup.bash
ros2 --version

# Verify Gazebo installation
gz sim --version

# Verify Node.js and npm
node --version
npm --version

# Verify Python environment
which python3
python3 --version
```

## Troubleshooting Common Issues

### Permission Denied Errors with Docker
After installing Docker, you may need to log out and log back in for group membership changes to take effect.

### ROS 2 Package Not Found
If ROS 2 commands are not recognized, ensure you've sourced the setup.bash file or added it to your shell profile:
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Next Steps

Once your environment is set up, proceed with the [Basic ROS 2 Tutorial](../ros2/basics.md) to familiarize yourself with the Robot Operating System.

---

Congratulations! Your development environment is now set up and ready for exploring Physical AI and Humanoid Robotics.