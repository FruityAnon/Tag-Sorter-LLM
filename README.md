# ⚠️ Disclaimer
**This project is developed solely for educational and personal purposes. It is intended to help new artists and ComfyUI users learn the principles of working with prompts and tags, as well as to automate personal creative projects.**

# LLM Tag Sorter Suite for ComfyUI
The LLM Tag Sorter Suite is a set of tools designed to automate and significantly improve the process of working with tags in ComyUI. This project solves one of the most tedious tasks in creating AI images: sorting and structuring dozens of tags to get the perfect prompt.

With an LLM-based sorter and convenient browser extensions, you can transform a chaotic set of tags into clearly organized categories.

![](images_rep\all_node.png)

## Workflow: How It Works
**Step 1:** Copying tags in the browser. Use the extension on one of the supported sites to instantly copy all image tags.

**Step 2**: Pasting and sorting in ComfyUI. Paste the copied tags into the ***Tag Sorter ✨*** node. The model will automatically analyze and distribute them into categories.

**Step 3 (Optional):** Combining the sorted tags. Connect the outputs from the `Tag Sorter ✨` with the `Text Blending 📦` node to assemble the categories into a single prompt, ready to be passed to the KSampler.

### 🛠️ Installation
Navigate to the `ComfyUI\custom_nodes\` directory.
Clone this repository using the command:

`git clone https://github.com/FruityAnon/Tag-Sorter-LLM.git`

The **Tag Sorter ✨** node has a built-in dependency manager and will automatically install `llama-cpp-python` on the first run.

## How to Use the Extension
Go to one of the supported sites:

1. https://e621.net/
2. https://rule34.xxx/
3. https://e6ai.net/

Open the page with the image whose tags you want to use. Click on the extension icon in your browser's toolbar. All tags will be automatically copied to your clipboard.

Paste the copied text into the `raw_tags` field in the **Tag Sorter ✨** node in ComfyUI.

## Installing the Browser Extensions

### **Google Chrome**
Open your browser and navigate to `chrome://extensions`.

In the top right corner, enable ***"Developer mode"***.

![In the top right corner, enable ***"Developer mode"***.](images_rep\chorme_developer_mode.png)

Click the ***"Load unpacked"*** button.

![](images_rep\chrome_Load_Unpacked.png)

Select the `comfyui_tag_importer_chrome` folder with the extension files, located at `Tag-Sorter-LLM\Browser-Universal-Tag-Copier\comfyui_tag_importer_chrome`.

### **Mozilla Firefox:**

Open your browser and navigate to `about:addons`.

Drag and drop the application file `comfyui_tag_importer_firefox.xpi`.

## 📖 Component Descriptions (Nodes)
### This suite contains three custom nodes for ComfyUI.

### Tag Sorter ✨

![](images_rep\node_tagSorter.png)

This node takes a single large string of tags and uses a local LLM to sort them into four categories:

**character:** Character description (appearance, body, facial features).

**clothing:** Clothing description (anything that can be worn, accessories).

**location:** Scene and pose (background, environment, character's position).

**enhancement:** Tags for improving image quality (style, lighting, detail).

### Text Blending 📦

![](images_rep\node_textBlending.png)

This node is for combining text blocks. It takes up to 6 strings and joins them into a single prompt, separated by the special keyword `BREAK`. This allows you to use the syntax for controlling prompt weights in ComfyUI.

### Text Hub 📝

![](images_rep\node_textHub.png)

This node acts as a "junction box" for text. It takes up to 6 text strings and passes them on. This helps keep large and complex workflows clean and organized, avoiding a "web" of connections.