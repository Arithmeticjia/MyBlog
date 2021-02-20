import { AxiosInstance } from "axios";
import MockAdapter from "axios-mock-adapter";

export let mock_axios: MockAdapter;

export function make_mock(axios_instance: AxiosInstance) {
  //mock 模拟数据
  mock_axios = new MockAdapter(axios_instance);

  //模拟工作流列表
  mock_axios
    .onGet("/api/wfs/workflow_list/WFFInfo")
    .reply(200, [{ wf_id: "a", date: "2020-9-1", name: "zc" }]);

  mock_axios
    .onGet("/api/wfs/workflow_list/WFTInfo")
    .reply(200, [{ wf_id: "b", date: "2020-9-1", name: "zc1" }]);

  mock_axios.onPost("/api/wfs/workflows/a/execute").reply(200, "zc");

  mock_axios
    .onGet("/api/wfs/workflowJobs/zc")
    .reply(
      200,
      '{[{"name": "A", "dependencies": {[]}, "id": "1", "template": "alpine: 3.7", "style_type": "success"}, {"name": "B", "dependencies": {["A"]}, "id": "2", "template": "alpine: 3.7", "style_type": "normal"}, {"name": "C", "dependencies": {["A"]}, "id": "3", "template": "alpine: 3.7", "style_type": "disable"}, {"name": "D", "dependencies": {["B", "C"]}, "id": "4", "template": "alpine: 3.7", "style_type": "success"}]}'
    );

  //模拟登录
  mock_axios.onPost("/api/users/login").reply(200, {
    access_token:
      "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjEyMyIsInVzZXJuYW1lIjoiaGFoYSIsImVtYWlsIjoiMTIzIiwicm9sZSI6MX0.SPjFd-QZ9TG9QHdA0_3Dz4hclw0PRUOBOqP401IlXQI",
    username: "管理员",
    stuid: "3220191001",
    role: "admin",
  });
}
