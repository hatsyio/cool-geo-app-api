from jinja2 import Template


class TemplateLoader:
    @staticmethod
    def load_template(filename) -> Template:
        with open("app/database/templates/" + filename) as f:
            return Template(f.read())
