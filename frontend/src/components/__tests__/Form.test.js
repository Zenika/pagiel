import { describe, expect, test } from "vitest";
import { render, screen } from "@testing-library/vue";
import Form from "../Form.vue";
import userEvent from "@testing-library/user-event";

describe("When I enter something in both inputs (URL & page name)", () => {
  test("I should be able to submit for analysis or add another page", async () => {
    render(Form);
    await userEvent.type(screen.getByPlaceholderText("URL"), "URL test");
    await userEvent.type(
      screen.getByPlaceholderText("Nom de la page"),
      "page name test"
    );
    expect(
      screen.getByRole("button", { name: "Ajouter une autre page" })
    ).not.toBeDisabled();
    expect(
      screen.getByRole("button", {
        name: "Analyser",
      })
    ).not.toBeDisabled();
  });
});

describe("When I enter something only in one input", () => {
  test("I should not be able to launch the analysis nor add the page to the current list of webpages", async () => {
    render(Form);
    await userEvent.type(screen.getByPlaceholderText("URL"), "URL test");
    expect(
      screen.getByRole("button", {
        name: "Ajouter une autre page",
      })
    ).toBeDisabled();
    expect(
      screen.getByRole("button", {
        name: "Analyser",
      })
    ).toBeDisabled();
  });

  test("I should not be able to add another page", async () => {
    render(Form);
    await userEvent.type(
      screen.getByPlaceholderText("Nom de la page"),
      "page name test"
    );
    expect(
      screen.getByRole("button", {
        name: "Ajouter une autre page",
      })
    ).toBeDisabled();
  });
});

describe("When I don't have any webpages saved and both my inputs are empty", () => {
  test("I should not be able to analyze anything", () => {
    render(Form);
    expect(screen.getByRole("button", { name: "Analyser" })).toBeDisabled();
  });
});

describe("When I do have webpages saved and one of the inputs is empty and the other one is filled", () => {
  test("I should not be able to run the analysis", async () => {
    render(Form);
    await userEvent.type(screen.getByPlaceholderText("URL"), "URL test");
    await userEvent.type(
      screen.getByPlaceholderText("Nom de la page"),
      "page name test"
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Ajouter une autre page" })
    );
    await userEvent.type(
      screen.getByPlaceholderText("URL"),
      "URL test number 2"
    );
    expect(screen.getByRole("button", { name: "Analyser" })).toBeDisabled();
  });
});

describe("When I do have webpages saved but both my inputs are empty", () => {
  test("I should be able to analyze the webpages saved", async () => {
    render(Form);
    await userEvent.type(screen.getByPlaceholderText("URL"), "URL test");
    await userEvent.type(
      screen.getByPlaceholderText("Nom de la page"),
      "page name test"
    );
    await userEvent.click(
      screen.getByRole("button", { name: "Ajouter une autre page" })
    );
    expect(screen.getByRole("button", { name: "Analyser" })).toBeEnabled();
  });
});
