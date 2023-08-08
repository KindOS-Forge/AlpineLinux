from jinja2 import Environment, FileSystemLoader


def render_template(template_name, variables={}, template_dir="templates"):
    # Load the templates from the template directory
    env = Environment(loader=FileSystemLoader(template_dir))

    # Load the template
    template = env.get_template(template_name)

    # Render the template with the provided variables
    rendered_output = template.render(variables)
    return rendered_output
