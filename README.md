<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS SSO Tool</title>
</head>
<body>

<h1>AWS SSO Tool</h1>
<p>A simple CLI tool to help developers connect to AWS via SSO and perform basic AWS operations, such as listing S3 buckets, uploading and downloading files, and managing EC2 instances. This tool ensures that AWS SSO tokens are automatically renewed when needed, streamlining the AWS login process for developers.</p>

<h2>Features</h2>
<ul>
    <li>Automatically handle AWS SSO login and token management.</li>
    <li>List S3 buckets in your AWS account.</li>
    <li>Upload files to and download files from S3.</li>
    <li>List EC2 instances and manage their state (start/stop).</li>
</ul>

<h2>Installation</h2>
<p>To install the <code>aws-sso-tool</code>, you can use <code>pip</code>:</p>

<pre><code>pip install aws-sso-tool</code></pre>

<p>This will install the tool and its dependencies.</p>

<h2>Usage</h2>
<p>Once the tool is installed, you can access it from the command line using the <code>aws-sso-tool</code> command. Below are the common commands and options available:</p>

<h3>Basic Commands</h3>

<ol>
    <li><strong>Set the Default AWS Profile</strong>
    <p>You can set or change the default AWS profile to be used for SSO authentication:</p>
    <pre><code>aws-sso-tool --set-default</code></pre>
    <p>This command will prompt you to enter your AWS profile name.</p>
    </li>

    <li><strong>Set or Change the AWS Region</strong>
    <p>You can set the default AWS region for operations:</p>
    <pre><code>aws-sso-tool --set-region</code></pre>
    <p>The command will fetch a list of available regions from AWS and prompt you to choose one.</p>
    </li>

    <li><strong>List S3 Buckets</strong>
    <p>List all S3 buckets in the connected AWS account:</p>
    <pre><code>aws-sso-tool --list-buckets</code></pre>
    <p>This will display all the S3 buckets under the connected AWS account.</p>
    </li>

    <li><strong>Upload a File to S3</strong>
    <p>Upload a file to a specific S3 bucket:</p>
    <pre><code>aws-sso-tool --upload-file &lt;file_path&gt; &lt;bucket_name&gt;</code></pre>
    <p>Optionally, you can provide an <code>object_name</code> to set the name of the file in S3:</p>
    <pre><code>aws-sso-tool --upload-file &lt;file_path&gt; &lt;bucket_name&gt; --object-name &lt;object_name&gt;</code></pre>
    </li>

    <li><strong>Download a File from S3</strong>
    <p>Download a file from a specific S3 bucket:</p>
    <pre><code>aws-sso-tool --download-file &lt;bucket_name&gt; &lt;object_name&gt; &lt;file_path&gt;</code></pre>
    <p>This command will download the file from S3 to the specified path.</p>
    </li>

    <li><strong>List EC2 Instances</strong>
    <p>List all EC2 instances in the selected AWS region:</p>
    <pre><code>aws-sso-tool --list-instances</code></pre>
    </li>

    <li><strong>Start an EC2 Instance</strong>
    <p>Start an EC2 instance by specifying its instance ID:</p>
    <pre><code>aws-sso-tool --start-instance &lt;instance_id&gt;</code></pre>
    </li>

    <li><strong>Stop an EC2 Instance</strong>
    <p>Stop an EC2 instance by specifying its instance ID:</p>
    <pre><code>aws-sso-tool --stop-instance &lt;instance_id&gt;</code></pre>
    </li>
</ol>

<h2>Configuration</h2>

<h3>AWS Profile</h3>
<p>The tool allows you to set the AWS profile you want to use with SSO. When you first run the tool, you'll be prompted to set the AWS profile. The profile will be saved to a local file and used as the default for subsequent operations.</p>

<h3>AWS Region</h3>
<p>Similarly, the tool will ask for your preferred AWS region the first time you run it. You can set or change the region using the <code>--set-region</code> command at any time.</p>

<h3>Automatic SSO Token Renewal</h3>
<p>The tool automatically checks the SSO token expiration and renews it if needed. It will only prompt for a login via the browser when necessary.</p>

<h2>Error Handling</h2>

<p>The tool handles various errors, such as:</p>
<ul>
    <li><strong>Invalid AWS credentials:</strong> If the AWS SSO token is expired or invalid, the tool will automatically attempt to renew it.</li>
    <li><strong>Connection issues:</strong> If there is an issue connecting to AWS, the error will be logged, and the user will be informed.</li>
    <li><strong>File not found:</strong> For file operations (upload/download), if the specified file path is invalid, the tool will log the error and inform the user.</li>
</ul>

<h2>Development</h2>

<p>To install the tool in development mode:</p>
<pre><code>pip install -e .</code></pre>

<h3>Running Tests</h3>
<p>You can run the tests using <code>pytest</code>:</p>
<pre><code>pytest tests/</code></pre>
<p>This will execute all the unit tests for the tool.</p>

<h2>Contributing</h2>
<p>Contributions are welcome! If you'd like to contribute, feel free to fork the repository and submit a pull request. Please make sure to write tests for any new functionality.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for more information.</p>

</body>
</html>
