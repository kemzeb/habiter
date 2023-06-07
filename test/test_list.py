import pytest
from click.testing import CliRunner

from habiter.internal.cli import habiter


@pytest.mark.usefixtures("setup")
def test_list(runner: CliRunner):
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0


@pytest.mark.usefixtures("setup")
def test_list_with_habits_in_record(runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    result = runner.invoke(habiter, ["list"])
    assert result.exit_code == 0
    assert "[t0]" in result.output


@pytest.mark.usefixtures("setup")
def test_list_with_habits_in_record_using_less_option(runner: CliRunner):
    runner.invoke(habiter, ["add", "t0", "t1"])
    result = runner.invoke(habiter, ["list", "-l"])
    assert result.exit_code == 0

    result = runner.invoke(habiter, ["list", "--less"])
    assert result.exit_code == 0


@pytest.mark.usefixtures("setup")
def test_list_passing_existing_habit_names_as_positional_args(runner: CliRunner):
    runner.invoke(habiter, ["add", "t0"])
    result = runner.invoke(habiter, ["list", "t0"])
    assert result.exit_code == 0
    assert "[t0]" in result.output


@pytest.mark.usefixtures("setup")
def test_list_passing_invalid_habit_names_as_positional_args(runner: CliRunner):
    result = runner.invoke(habiter, ["list", "t1", "t99"])
    assert result.exit_code == 1
