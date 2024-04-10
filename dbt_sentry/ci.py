import click


@click.group()
def ci():
    """Publish the audit report."""
    pass


@ci.command()
def generate():
    """Generates the audit report."""

    # 1. detect git file changed
    # 2. find all model that can be impacted (model+)
    # 3. run audit xx for models
    # 4. generate report output

    pass


@ci.command()
def publich_gitlab():
    """Publishes the audit report to gitlab."""
    pass


@ci.command()
def publish_github():
    """Publishes the audit report to github."""
    pass
