import { Button, Form, Input, Modal, Table, TableColumnsType, Tag } from "antd";
import Navbar from "./Navbar";
import { PlusIcon } from "@heroicons/react/24/outline";
import { useEffect, useState } from "react";
import FormItem from "antd/es/form/FormItem";
import instance from "axios-instance";
import { notification } from "antd";

interface DataType {
  id: string;
  name: string;
  connection: string;
  status: string;
}

type FormValues = {
  name: string;
  connection: string;
}

const Pipeline = () => {
  const [api, contextHolder] = notification.useNotification();
  const [isActionOpen, setIsActionOpen] = useState(false);
  const [pipelines, setPipelines] = useState<DataType[]>([]);

  useEffect(() => {
    try {
      instance({
        url: "pipeline",
        method: "GET",
      })
      .then((res) => {
        // handle success
        setPipelines(res.data.pipelines)
        console.log(res);      
        
      });
    } catch (e) {
      // handle error
      console.error(e);
      api.info({
        message: 'Error Occured', 
        placement: 'topRight',
      });
    } 
  },[])

  const columns: TableColumnsType<DataType> = [
    {
      title: "Name",
      dataIndex: "name",
      render: (text: string, record: DataType) =>  <a href={`/pipeline/${record.id}`}>{text}</a>
    },
    {
      title: "Connection",
      dataIndex: "connection",
    },
    {
      title: "Status",
      dataIndex: "status",
      render: (_, { status }) => (
        <>  <Tag color={ status === 'completed' ? 'green' : 'blue'}>
                {status.toUpperCase()}
              </Tag>             
        </>
      ),
    },
  ];

  const createPipeline = async (formValues: FormValues) => {
    var data = {
      name: formValues.name,
      connection: formValues.connection,
    };
    try {
      await instance({ 
        url: "pipeline/create",
        method: "POST",
        data: data,
      }).then((res) => {
        // handle success
        console.log(res);
        api.info({
          message: res.data.message, 
          placement: 'topRight',
        });

        setTimeout(() => {
          window.location.reload();
        },2000)
      });
    } catch (e) {
      // handle error
      console.error(e);
    }
  }
 

  return (
    <>
      <main className="ml-64 flex-1 bg-white dark:bg-dark-bgColor">
        <Navbar title={"Pipelines"} />
        <div className="relative pt-20 px-10 w-full flex h-screen flex-col p-4">
          <Button className="w-28" 
        onClick={() => setIsActionOpen(true)}          
          color="default" variant="filled">
            Add Pipeline
          </Button>
          <br />
          <Table<DataType>
            rowSelection={{ type: "checkbox" }}
            columns={columns}
            dataSource={pipelines ?? []}
          />
        </div>
      </main>

      <Modal
        style={{ top: "5rem" }}
        open={isActionOpen}
        footer={false}
        onCancel={() => setIsActionOpen(false)}
      >
        <h1 className="text-xl font-medium dark:text-dark-textColor">
          Create Pipeline
        </h1>
        <br />

        <div className={"min-h-auto max-h-[36rem] space-y-6 overflow-y-auto"}>
        <Form onFinish={createPipeline}>
        <Form.Item<FormValues>
        label="Name"
        name="name"
        rules={[{ required: true, message: 'Please input your name!' }]}
        >
        <Input />
        </Form.Item>

        <Form.Item<FormValues>
        label="Connection"
        name="connection"
        rules={[{ required: true, type: 'url' }, {warningOnly: true}, {message: 'Please input your connection!' }]}
        >
        <Input />
        </Form.Item> 
      <Button color="default"  variant="filled" htmlType="submit">
        Submit
      </Button> 

        </Form>
        </div>
      </Modal>

    </>
  );
};
export default Pipeline;
