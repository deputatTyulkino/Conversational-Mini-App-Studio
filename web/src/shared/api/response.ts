import type { AxiosResponse } from "axios";

export type ApiResponse<T> = { data: T };

export const unwrap = <T>(response: AxiosResponse<ApiResponse<T>>) =>
  response.data.data;
