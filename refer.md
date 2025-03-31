What is MCP
Think of MCP as a USB C port on a laptop. With it, you can charge your laptop, perform data transfer, connect to other displays, and charge other Type C-supported devices as well.

Similarly, Model Context Protocol (MCP) provides a standard, secure, real time, and two-way communicating interface to AI systems for connecting with external tools, API Services and data sources.

What it means is, unlike traditional APIs integration which requires separate code, documentation, authentication methods, and maintenance, MCP can provide a single, standardized way for AI models to interact with external systems, i.e. you write code once and all AI systems can use it.

The key differences between MCP and traditional APIs include:

Feature	MCP	Traditional API
Integration Effort	Single, standardized integration	Separate integration per API
Real-Time Communication	✅ Yes	❌ No
Dynamic Discovery	✅ Yes	❌ No
Scalability	Easy (plug-and-play)	Requires additional integrations
Security & Control	Consistent across tools	Varies by API
MCP enables two-way communication, allowing AI models to both retrieve information and trigger actions dynamically. This makes it perfect for creating more intelligent and context-aware applications.

So how this all works?

MCP Components
MCP Workings

The MCP architecture consists of several key components that work together to enable seamless integration:

MCP Hosts: These are applications (like Claude Desktop or AI-driven IDEs) that need access to external data or tools
MCP Clients: They maintain dedicated, one-to-one connections with MCP servers.
MCP Servers: Lightweight servers that expose specific functionalities via MCP, connecting to local or remote data sources.
Local Data Sources: Files, databases, or services securely accessed by MCP servers
Remote Services: External internet-based APIs or services accessed by MCP servers
This separation of concerns makes MCP servers highly modular and maintainable.

So how this all connect?

How The Components Work Together
Let’s understand this with a practical example:

Say you're using Cursor (an MCP host) to manage your project's budget. You want to update a budget report in Google Sheets and send a summary of the changes to your team via Slack.

Cursor (MCP host) initiates a request to its MCP client to update the budget report in Google Sheets and send a Slack notification.
The MCP client connects to two MCP servers: one for Google Sheets and one for Slack.
The Google Sheets MCP server interacts with the Google Sheets API (remote service) to update the budget report.
The Slack MCP server interacts with the Slack API (remote service) to send a notification.
MCP servers send responses back to the MCP client.
The MCP client forwards these responses to Cursor, which displays the result to the user.
This process happens seamlessly, allowing Cursor to integrate with multiple services through a standardized interface.

But understanding fundamental is no use if one can’t build, so let’s get building!

How to Build a MCP Server
There are 2 ways to build a MCP Server, using Python SDK or JavaScript SDK, for sake of simplicity, I will stick to Python SDK.

So, like any other good dev, let’s create a separate work environment to keep things isolated.

1. Work Environment Setup
We start by creating a project directory.

Navigate to your working folder and create a folder named mcp or u can use the terminal command:

mkdir mcp
cd mcp
Next create a virtual environment using:

# windows 
python -m venv dotenv

# linux/mac
python -m venv --help
sudo apt-get install python3-venv #install venv - optional
python3 -m venv dev-env
Now activate the environment with:

# activates env
dotenv\Scripts\activate

# linux/mac
dotenv\Scripts\activate
Ensure you see (dotenv) Infront of the terminal cwd path.

Finally install 2 libraries - MCP SDK, MCP CLI:

# install libraries
pip install mcp mcp[cli]
It might ask you permission to install, press y and once installed, we are done with setting up the environment

2. Writing the Server Code
Open the folder in any of your favourite editors of choice, create a new file called calculator.py, and write the following code:

# basic import 
from mcp.server.fastmcp import FastMCP
import math

# instantiate an MCP server client
mcp = FastMCP("Hello World")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return int(a + b)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    return float(math.tan(a))

# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


 # execute and return the stdio output
 if __name__ == "__main__":
    mcp.run(transport="stdio")

Ok, so let’s take a moment to understand what's happening in the code.

First, we imported the FastMCP server from the MCP package and the math module. The FastMCP Server manages connections, follows the MCP protocol, and routes messages.
Next, we created an MCP server client and named it "Hello World" 😂.
Then, we added tools using @mcp.tool() and resources using @mcp.resource(). These tools help the server perform operations, and the resource provides personalized greetings. (talk about exposing your data to LLM*)*
Lastly, we start the mcp-server using @mcp.run(), and the setup allows communication via standard input/output (stdio).
Hopefully, you will clearly understand what the code is doing now!

Now let’s test it using MCP Inspector

3. Running & Testing the Server Locally
MCP Inspector is a handy GUI tool that lets you test your custom MCP server without integrating it with LLM / AI agents. Let’s set it up.

Follow the steps to run and debug the program using mcp server locally.

Open the terminal and ensure you are in the working environment.
Run mcp dev calculator.py.
If prompted, install CLI by pressing ‘y’ or do it manually, then rerun the command.
Open the displayed URL (mostly localhost) and press "Connect" in MCP Inspector.
If an error occurs, restart your PC and rerun the command.
Click "List Templates", select one, add your name, and click "Read Resources".
Check the displayed output.
Click on "Tools" in the navbar.
Click "List Tools", choose one, input values, and press "Run Tool".
NOTE: If a Pydantic error appears, delete both values and enter new ones.

So, with this, we are done with testing.

However real power of MCP lies with the integration of IDE’s / Agents. Let’s look at how to connect them?

Connecting Custom Servers to Cursor
I will use Cursor for demonstration purposes, as integration is simple and straightforward. Follow these steps for the integration

Open your current working directory (cwd) in Cursor.
Activate the virtual environment (optional but recommended).
Go to File → Preferences → Cursor Settings → MCP → Add New Server.
Fill in the server details:

Name: Choose a name (e.g., "calculator").
Type: Set as command.
Command: Provide the full command to run the server:
/path/to/your/venv/bin/python /path/to/your/file.py
Run the configuration and check for a 🟢 calculator indicator.

If the indicator is 🟠, verify and correct the file paths.

Open the composer, select "Agent", and type:

Can you add two numbers 3, 6
Check if the mcp_add() tool is automatically retrieved.

Test the server tools in Cursor for supported functionality.

So far, so good, but these are just toy examples. What if you have to work on some advanced projects and use multiple different servers/tools? You'd need to write multiple lines of code for multiple tools, right?

Let’s look at a simpler alternative and how its one-liner integrations simplify workflow.

Enters Composio!

Composio in a Nutshell
Composio is the ultimate integration platform, empowering developers to seamlessly connect AI agents with external tools, servers, and APIs with just a single line of code.

With the fully managed MCP Servers, developers can rapidly build powerful AI applications without the hassle of managing complex integrations. We take care of the infrastructure so you can focus on innovation.

Let’s dive into how you can integrate composite-mcp into your workflow effortlessly!

Composio MCP Integration
Integrating with Composio MCP is incredibly simple and can be done in just five steps:

Visit the Composio MCP Directory page
Select Tools you need, keep an eye on the following: Name: Name of tool / Server Description: What the tool does Images: Compatibility (as of now, Windsurf isn’t available for Windows)
Go to the Installation Steps section on the next page and hit Generate. Copy the generated URL (private info). Make sure to read all the available functions in the Available Actions section.
Open the cursor and head over to File → Preferences → Cursor Settings → MCP → Add New Server
Select Type as “sse” & paste the copied URL into the Server URL. & you are done!
To test the integration, go to the Composer, initiate a connection, and ask it to perform actions by prompting like in previous section.

Let’s look at an advanced integration to see where composio-mcp shines.

Linear tickets Management with Slack Collaboration.
Composio can handle advanced use cases effortlessly. Let’s demonstrate how Composio solves the following challenge seamlessly:

Development teams often struggle to manage product-related issues, as this requires constant back-and-forth between the IDE and team Slack channels.
Develop an agent that handles all the operations through the IDE. This way, teams can stay in sync without unnecessary context switching, dramatically increasing productivity.

Let’s use composio-mcp for this one!

We will create a linear ticket for demonstration purposes and send it to our Slack team channel.

Follow the steps one after another:

Head to the MCP Repository and select Linear & Slack integrations. If you don’t find them listed, use the search console.
Generate an SSE Key & copy it.
Open the cursor and integrate it with the method covered in the above section.
Integrating Linear & Slack in Cursor.
Ok, now let’s see if it works as expected.

Head to the cursor chat and select Agent.
Initiate an OAuth connection by writing “create a connection with Slack”.
Do the same for Linear Head to the generated URL and authenticate.
Once done, head back to the cursor and ask if the connection is active.
Make sure to review the permission once!

Once everything is in place, you can start working with the MCP integrations.

Head to the cursor chat and select Agent.
Initiate an OAuth connection by writing “create a connection with Slack”. Do the same for Linear
Head to the generated URL and authenticate. Make sure to review the permission! slack-oauth.mp4
Once done, head back to the cursor and ask if the connection is active.
Once everything is in place, you can start working with the MCP integrations.
slack-composio-integration

Conclusion
As AI transforms software development, MCP will play an increasingly important role in creating seamless, integrated experiences.

Whether you're building custom MCP servers or leveraging pre-built solutions like Composio MCP, the protocol offers a powerful way to enhance AI capabilities through external tools and data sources.

The future of AI isn't just about smarter models - it's about creating ecosystems where AI can seamlessly interact with the tools we use every day. MCP is a crucial step toward that future.

I hope you had a great learning experience—happy building with Composio! 🚀