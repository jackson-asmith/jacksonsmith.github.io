# Parse the YAML front matter of every tracked Markdown and HTML file the
# way Jekyll does. Jekyll doesn't fail the build on invalid front matter: it
# warns and drops the page's settings, so a stray ": " in a description can
# quietly change how a page renders. This turns that into a failed check.
require "yaml"
require "date"

files = `git ls-files -- '*.md' '*.markdown' '*.html'`.split("\n")
bad = 0
files.each do |path|
  text = File.read(path, encoding: "UTF-8")
  front = text[/\A---\s*\n(.*?)\n---\s*$/m, 1]
  next unless front
  begin
    YAML.safe_load(front, permitted_classes: [Date, Time], aliases: true)
  rescue Psych::Exception => e
    bad += 1
    puts "::error file=#{path}::Invalid front matter: #{e.message}"
  end
end
puts "Checked #{files.size} files, #{bad} with invalid front matter."
exit(bad.zero? ? 0 : 1)
