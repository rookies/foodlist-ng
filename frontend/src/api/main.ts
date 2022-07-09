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
  list_items(params: object) {
    const query_string = Object.keys(params).map((key) => {
      return encodeURIComponent(key) + "=" + encodeURIComponent(params[key])
    }).join("&");
    return request("GET", "/items?" + query_string);
  },
  delete_item(id: number) {
    return request("DELETE", "/items/" + id);
  },
  update_item(id: number, values: object) {
    return request("PATCH", "/items/" + id, values);
  },
  create_tag(item_id: number, tag: string) {
    return request("POST", "/items/" + item_id + "/tags/" + encodeURIComponent(tag));
  },
  delete_tag(item_id: number, tag: string) {
    return request("DELETE", "/items/" + item_id + "/tags/" + encodeURIComponent(tag));
  },
};
