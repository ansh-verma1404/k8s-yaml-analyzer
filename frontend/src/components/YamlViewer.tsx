import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { duotoneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

interface Props {
  yamlText: string;
}

const YamlViewer: React.FC<Props> = ({ yamlText }) => {
  if (!yamlText) return null;
  return (
    <div style={{ marginTop: "1rem" }}>
      <h2>YAML Preview</h2>
      <SyntaxHighlighter language="yaml" style={duotoneDark}>
        {yamlText}
      </SyntaxHighlighter>
    </div>
  );
};

export default YamlViewer;
