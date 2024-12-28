# **Tools**

## **Overview**

Tools are integral components that empower Nevron to interact with external services and execute specific actions. 

Each tool is purpose-built to handle a distinct functionality, enhancing the agent's versatility and capability. Tools act as modular utilities that can be seamlessly integrated into workflows to perform specialized tasks. They enable connectivity with external services, third-party APIs, search engines, custom functions, and more.

All tools are organized within the `src/tools/` directory.

---

## **Available Tools**

### 1. Twitter Integration

The Twitter integration tool automates the publishing of content on Twitter, providing seamless connectivity for social media interactions.

### 2. Perplexity Integration

The Perplexity integration tool facilitates research and content analysis, leveraging Perplexity’s capabilities to enrich the agent's knowledge base.

### 3. Signal Processing

The Signal Processing tool enables the analysis of market signals and supports automated decision-making based on the processed data.

### 4. Telegram Integration

The Telegram integration tool automates the publishing of content on Telegram, streamlining communication and content delivery.

---

## **Adding a New Tool**

Adding a new tool is a straightforward process, following these steps:

1. Create a new file, e.g. `new_tool.py`, in the `src/tools/` directory.
2. Implement the tool's functionality.
3. Extensively test the tool to ensure it works as expected.

Once the tool is ready, it can be used in workflows to perform specialized tasks.