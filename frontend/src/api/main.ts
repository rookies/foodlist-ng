import { APISettings } from "./config.ts";

function request(method: string, path: string, json_data: object | null = null) {
  let params = {};
  if (json_data !== null) {
    params = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(json_data),
    };
  } else {
    params = {
      method: method,
    };
  }

  return fetch(APISettings.baseURL + path, params)
    .then((response) => {
      if (response.status !== 200) {
        throw response.status;
      } else {
        return response.json();
      }
    });
}

export default {
  list_items() {
    return request("GET", "/items");
  },
  delete_item(id: number) {
    return request("DELETE", "/items/" + id);
  },
  update_item(id: number, values: object) {
    return request("PATCH", "/items/" + id, values);
  },
};
