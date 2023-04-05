from click.testing import CliRunner

from habiter.internal.cli import habiter


def test_list(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0


def test_list_with_habits_in_record(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0
    assert "t0" in result.output


def test_list_with_habits_in_record_using_verbose_option(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0", "t1"])
    result = runner.invoke(habiter, ["list", "-v"])
    assert result.exit_code == 0

    result = runner.invoke(habiter, ["list", "--verbose"])
    assert result.exit_code == 0


def test_list_passing_existing_habit_names_as_positional_args(setup, runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    result = runner.invoke(habiter, ["list", "t0", "-v"])
    assert result.exit_code == 0
    assert "[t0]" in result.output


def test_list_passing_invalid_habit_names_as_positional_args(setup, runner: CliRunner):
    result = runner.invoke(habiter, ["list", "t1", "t99", "-v"])
    assert result.exit_code == 1
