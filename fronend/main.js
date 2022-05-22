$(() => {
  const enpoind = "http://127.0.0.1:5000/v1/";
  const table = $("#gridContainer");
  const chartCtx = $("#badCanvas1");
  const generarNumero = (numero) => {
    return (Math.random() * numero).toFixed(0);
  };

  const colorRGB = () => {
    let coolor =
      "(" +
      generarNumero(255) +
      "," +
      generarNumero(255) +
      "," +
      generarNumero(255) +
      ")";
    return "rgb" + coolor;
  };
  const innerLabelBlob = () => {
    $.ajax({
      url: enpoind + "storage/location",
      success: function ({ data }) {
        const div = document.createElement("div");
        div.className = "alert alert-light";
        div.setAttribute("role", "alert");

        for (const key in data) {
          if (Object.hasOwnProperty.call(data, key)) {
            let element = data[key];
            const span = document.createElement("span");
            const p = document.createElement("p");
            span.className = "span-b";
            span.appendChild(document.createTextNode("Archivo " + key + " "));
            p.appendChild(span);
            p.appendChild(document.createTextNode(element));
            div.appendChild(p);
          }
        }
        $("#lable-blob").append(div);
      },
    });
  };

  const renderChart = ({ data }) => {
    const config = generateConfigChart(data);

    const myChart = new Chart(chartCtx, config);
  };

  const generateConfigChart = (data) => {
    let labels = [];
    let series = {},
      datasets = [];

    for (let item in data) {
      labels.push(item);
      Object.keys(data[item]).forEach((itemkey) => {
        if (series[itemkey] === undefined) {
          series[itemkey] = [];
        }
        series[itemkey].push(data[item][itemkey]);
      });
    }
    for (let item in series) {
      datasets.push({
        label: item,
        data: series[item],
        backgroundColor: colorRGB(),
      });
    }
    return {
      type: "bar",
      data: {
        labels: labels,
        datasets: datasets,
      },
      options: {
        indexAxis: "y",

        elements: {
          bar: {
            borderWidth: 2,
          },
        },
        responsive: true,
        plugins: {
          legend: {
            position: "right",
          },
          title: {
            display: true,
            text: "Grafica de  Análisis",
          },
        },
      },
    };
  };
  $("#btn2").click(() => {
    table.hide();
    chartCtx.show();
    $.ajax({
      url: enpoind + "storage/chart",
      success: renderChart,
    });
  });

  innerLabelBlob();
  $("#btn1").click(() => {
    chartCtx.hide();
    table.show();
    table.dxDataGrid({
      dataSource: {
        store: {
          type: "odata",
          url: enpoind + "storage/",
        },
      },
      paging: {
        pageSize: 10,
      },

      remoteOperations: false,
      filterRow: {
        visible: true,
        applyFilter: "auto",
      },
      searchPanel: {
        visible: true,
        width: 240,
        placeholder: "Buscar en la tabla",
      },
      headerFilter: {
        visible: true,
      },
      groupPanel: {
        visible: true,
        emptyPanelText: "Arrastre la coluna para  agrupar",
      },
      grouping: {
        autoExpandAll: false,
      },

      allowColumnReordering: true,
      rowAlternationEnabled: true,
      showBorders: true,
      columns: [
        {
          dataField: "Nombre",
          dataType: "string",
        },
        {
          dataField: "Apellido",
          dataType: "string",
        },
        {
          dataField: "Nombre Completo",
          dataType: "string",
        },
        {
          dataField: "Cedula",
          dataType: "string",
        },
        {
          dataField: "Edad",
          dataType: "string",
        },
        {
          dataField: "Nacimiento",
          dataType: "date",
        },
        {
          dataField: "Tipo de pedido",
          dataType: "string",
        },
        {
          dataField: "Numero de pedido",
          format: "currency",
          alignment: "right",
          width: 150,
        },
      ],
    });
  });
});
