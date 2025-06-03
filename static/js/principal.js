window.onload = () => {
    const fileElement = document.querySelector('#file-upload');
    const algBtn1 = document.querySelector('#algorithm-btn1');
    const algBtn2 = document.querySelector('#algorithm-btn2');
    const algBtn3 = document.querySelector('#algorithm-btn3');
    const algBtn4 = document.querySelector('#algorithm-btn4');
    const modelSaveBtn = document.querySelector('#save-model-btn');
    const mfContainer = document.querySelector('.model-form-container');
    const btnCloseForm = document.querySelector('#close-form-btn');

    var gcleandata = null;
    var gparams = null;

    // Presenta el nombre del archivo al lado y muestra tabla
    const uploadFile = () => {
        const csvFile = fileElement.files[0];
        const filename = csvFile.name;
        
        const loadingTable = document.querySelector('#loading-table');
        
        //document.querySelector('#tabla').innerHTML = "";
        loadingTable.classList.add('lt-open');
        
        const formData = new FormData();
        formData.append('dataFile', csvFile);
        formData.append('dataName', filename);
        fetch('/file/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            if(data.ok){
                let datos = data.datos;
                loadingTable.classList.remove('lt-open');
                sessionStorage.setItem('filename', datos.nombre_archivo);
                sessionStorage.setItem('datapages', datos.paginas);
                
                readFile(datos.nombre_archivo);
                //POR REVISAR
                //previewData(filename, data, "#tabla");
    
                //sessionStorage.setItem('data', JSON.stringify(data));
            }
        });
        
    }

    // Presenta el nombre del archivo al lado y muestra tabla
    const readFile = (archivo, pagina=1) => {
        construirNav(pagina);
        const loadingTable = document.querySelector('#loading-table');
        
        document.querySelector('#tabla').innerHTML = "";
        loadingTable.classList.add('lt-open');

        let queries = "?pagina="+pagina
        
        const formData = new FormData();
        formData.append('filename', archivo);
        fetch('/file/read'+queries, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingTable.classList.remove('lt-open');
            previewData(archivo, data, "#tabla");
        });
        
    }

    const construirNav = (actual=1) => {
        let paginas = parseInt(sessionStorage.getItem('datapages'));
        let maxnavs = 10
        let pagesAnt = 8

        let inicio = 1;
        //let fin = inicio + maxnavs;
        let fin = paginas+1;

        if((actual-pagesAnt) > 0){
            inicio = actual - pagesAnt;
        }

        if((inicio + maxnavs) <= paginas+1){
            fin = inicio + maxnavs;
        }

        console.log(inicio, ' => ', fin)

        //let htmlnav = ""
        $('#data-pages').empty();
        for(let i=inicio; i<fin; i++){
            //htmlnav += `<li class="page-item"><a class="page-link paginado-data" id="navpage-${i}" pagina="${i}" href="#" onclick="clickPagina(this)">${i}</a></li>`;
            let $lista = $('<li>')
                .addClass('page-item');

            var $link = $('<a>')
                .addClass('page-link paginado-data')
                .attr('id', `navpage-${i}`)
                .attr('pagina', i)
                .attr('href', '#')
                .text(i);

            $link.on('click', function() {
                clickPagina(this);
            });
            //let link = $(`<a class="page-link paginado-data" id="navpage-${i}" pagina="${i}" href="#" onclick="clickPagina(this)">`).text(i);
            $lista.append($link)
            $('#data-pages').append($lista);
        }
        //$('#data-pages').html(htmlnav);
        //$('.page-item').removeClass('active')
        $(`#navpage-${actual}`).parent().addClass('active');
    }

    const openForm = (event) => {
        mfContainer.style.display = "flex";
        setTimeout(()=>{
            showForm(event.srcElement);
            mfContainer.classList.add('mf-container-open');
        }, 100);
    }

    const closeForm = (event) => {
        mfContainer.style.display = 'none';
        document.querySelector('#data-model-preview').style.display = "none";
        mfContainer.classList.remove('mf-container-open');
        document.querySelector('#body-alg-form').innerHTML = "";
    }
    
    fileElement.addEventListener('change', uploadFile);
    algBtn1.addEventListener('click', openForm);
    algBtn2.addEventListener('click', openForm);
    algBtn3.addEventListener('click', openForm);
    algBtn4.addEventListener('click', openForm);
    btnCloseForm.addEventListener('click', closeForm);

    /*$('.paginado-data').on('click', function() {
        //$('.page-item').removeClass('active')
        //$(this).parent().addClass('active');

        let datoscsv = sessionStorage.getItem('filename');

        if(datoscsv){
            var valor = $(this).attr('pagina');
            readFile(datoscsv, valor);
        }
    });*/

    const clickPagina = (elemento) => {
        console.log(elemento);
        let datoscsv = sessionStorage.getItem('filename');

        if(datoscsv){
            var valor = $(elemento).attr('pagina');
            readFile(datoscsv, valor);
        }
    }

    if(sessionStorage.getItem('filename')){
        //let data = JSON.parse(sessionStorage.getItem('data'));
        let filename = sessionStorage.getItem('filename');
        readFile(filename);
    }

    document.querySelector('#form-btn-preview').addEventListener('click', (e) => {
        document.querySelector('#data-model-preview').style.display = "block";
        document.querySelector('#data-model-preview').style.height = `${document.querySelector('#params-form').clientHeight}px`;

        //let data = sessionStorage.getItem('data');
        let filename = sessionStorage.getItem('filename');
        let algType = document.querySelector('#data-model-key').value;
        let colClase = document.querySelector('#clase-cols-select').value;
        let vcols = [];
        
        document.querySelectorAll('.data-cols:checked').forEach((elem) => vcols.push(elem.value));
        
        const loadingTable = document.querySelector('#loading-prev-mtable');
        
        document.querySelector('#prev-tabla').innerHTML = "";
        loadingTable.classList.add('lt-open');

        const formData = new FormData();
        //formData.append('data', JSON.stringify(data));
        formData.append('filename', filename);
        // formData.append('colClase', colClase);
        // formData.append('columnas', vcols);

        fetch(`/preview?metodo=${algType}&filename=${filename}&colClase=${colClase}&columnas=${vcols}`, {
            method: 'GET',
            //body: formData,
            headers:{
                'Content-Type': 'application/json',  // Asegúrate de que el servidor reciba JSON
            },
        })
        .then(response => response.json())
        .then(data => {
            loadingTable.classList.remove('lt-open');
            previewData(null, data, "#prev-tabla");
        });
    });
    
    document.querySelector('#form-btn-process').addEventListener('click', (e) => {
        //let data = sessionStorage.getItem('data');
        let filename = sessionStorage.getItem('filename');
        let algType = document.querySelector('#data-model-key').value;
        let colClase = document.querySelector('#clase-cols-select').value;
        let vcols = [];
        
        document.querySelectorAll('.data-cols:checked').forEach((elem) => vcols.push(elem.value));

        const formData = new FormData();
        //formData.append('data', data);
        formData.append('filename', filename);
        formData.append('colClase', colClase);
        formData.append('columnas', vcols);

        parametros = ""
        switch(algType){
            case 'knn': {
                let k = parseInt(document.querySelector('#k-neighbors-input').value);
                let centro = [
                    parseInt(document.querySelector('#k-centerx-input').value),
                    parseInt(document.querySelector('#k-centery-input').value)
                ];

                parametros += "&k="+k+"&centro="+centro.join(',')

                //formData.append('k', k);
                //formData.append('centro', centro);
                break;
            }

            case 'kmeans': {
                let n = parseInt(document.querySelector('#k-clusters-input').value);

                parametros += "&n="+n
                //formData.append('n', n);
                break;
            }
            
            default: {
                console.log("Accion no encontrada.")
            }
        }
        
        closeForm();
        fetch(`/process?metodo=${algType}&filename=${filename}&colClase=${colClase}&columnas=${vcols}${parametros}`, {
            method: 'GET',
            //body: JSON.stringify(data),
            headers:{
                'Content-Type': 'application/json',  // Asegúrate de que el servidor reciba JSON
            }
        })
        .then(response => response.json())
        .then(data => {
            let resHTML = `
                <div class="model-graph">
                    <img src="data:image/png;base64,${data['plot']}" id="model-result-graph" name="modelplot_${data['algType']+'_'+Date.now()}" width="100%" alt="Plot">
                </div>
            `;
            if(data['algType'] == "knn"){
                resHTML += `
                    <div class="model-result">
                        <p><b>Predicción:</b> ${data['prediction']}</p>
                        ${data['res_details']}
                    </div>
                `;
            }else if(data['algType'] == "kmeans"){
                resHTML += `
                    <div class="model-result">
                        <p><b>Resultado:</b> Algoritmo Kmeans</p><br>
                        ${data['res_details']}
                    </div>
                `;
            }else if(data['algType'] == "tree"){
                resHTML += `
                    <div class="model-result">
                        <p><b>Resultado:</b> Algoritmo Arbol de Decision</p><br>
                        ${data['res_details']}
                    </div>
                `;
            }else if(data['algType'] == "regression"){
                resHTML += `
                    <div class="model-result">
                        <p><b>Resultado:</b> Algoritmo Regresion</p><br>
                        ${data['res_details']}
                    </div>
                `;
            }
            const dataResult = document.querySelector('#data-result-content');
            dataResult.innerHTML = resHTML;
            document.querySelector("#save-model-btn").removeAttribute('disabled');

            document.querySelector('#save-alg-type').innerText = data['algType'];

            gcleandata = data['cleandata'];
            gparams = data['details'];
            previewData(null, JSON.parse(data['cleandata']), "#save-model-data");
            dataDetails = document.querySelector('#data-details');
            dataDetails.innerHTML = `
                <p><b>Tipo de Algoritmo:</b> <span id="d-algType">${data['algType']}</span></p>
                <p><b>Nombre de archivo:</b> <span id="d-filename">${data['filename']}</span></p>
            `;

            if(data['algType'] == "knn"){
                dataDetails.innerHTML += `
                <div id="d-more-details">
                    <p><b>Vecinos:</b> <span class="dmd-props" name="vecinos">${JSON.parse(data['details'])['k']}</span></p>
                    <p><b>Centro:</b> <span class="dmd-props" name="centro">(${JSON.parse(data['details'])['centro']})</span></p>
                </div>
                `
            }else if(data['algType'] == "kmeans"){
                dataDetails.innerHTML += `
                <div id="d-more-details">
                    <p><b>Clusters:</b> <span class="dmd-props" name="clusters">${JSON.parse(data['details'])['n']}</span></p>
                </div>
                `
            }
        });
    });

    modelSaveBtn.addEventListener('click', e => {
        document.querySelector('#save-form-container').style.display = 'flex';
    });

    document.querySelector('#close-sform-btn').addEventListener('click', e => {
        document.querySelector('#save-form-container').style.display = 'none';
    });

    document.querySelector('#save-name-model').addEventListener('input', e =>{
        let elem = e.target;
        let elBtnSave = document.querySelector('#btn-confirm-save');

        if(elem.value.trim() == ''){
            elBtnSave.setAttribute('disabled', 'true');
        }else{
            elBtnSave.removeAttribute('disabled');
        }
    })

    document.querySelector('#btn-confirm-save').addEventListener('click', e =>{
        let tipo = document.querySelector('#data-details #d-algType').innerText;
        let nombre = document.querySelector("#save-name-model").value;
        let archivo = document.querySelector('#data-details #d-filename').innerText;
        let datos = JSON.stringify(gcleandata);
        let params = JSON.stringify(gparams);

        let graphencode = document.querySelector('#model-result-graph').src.split(',')[1];
        let graphname = document.querySelector('#model-result-graph').getAttribute('name');

        const loadingSaveForm = document.querySelector('#loading-save-form');
        loadingSaveForm.classList.add('lt-open');

        const formData = new FormData();
        formData.append('tipo', tipo);
        formData.append('nombre', nombre);
        formData.append('archivo', archivo);
        formData.append('datos', datos);
        formData.append('params', params);
        formData.append('graphencode', graphencode);
        formData.append('graphname', graphname);

        fetch(`/model/save`, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
            
            loadingSaveForm.classList.remove('lt-open');
            document.querySelector('#save-form-container').style.display = "none";
            document.querySelector('#save-name-model').value = "";
            
            const responseAlert = document.querySelector('#response-alert-container');
            responseAlert.classList.add(`alert-${data['code']}`);
            document.querySelector('#alert-msg').innerText = data['msg'];

            responseAlert.classList.remove("hidden");

            setTimeout(() => {
                responseAlert.classList.add("hidden");
            }, 3000);
        });
    });
}

/* PRESENTA LOS DATOS EN FORMATO DE TABLA */
const previewData = (fname=null, data, tableId) => {

    /* FORMATEO DEL NOMBRE DE ARCHIVO EN LA CABECERA DE LA TABLA */
    if(fname && tableId=="#tabla"){
        document.querySelector("#filename-text").innerHTML = `<i class="fa-solid fa-file-csv"></i> ${fname}`;
        document.querySelector("#filename-text").style.padding = "0 10px";
        document.querySelectorAll('.btn-ia-model.allowed').forEach(el => {
            el.removeAttribute('disabled');
        })
    }

    /* FORMATEO DE LOS DATOS EN UNA TABLA */
    // Crear las cabeceras de la tabla
    let headers = Object.keys(data[0]);
    let headerRow = '<tr>';
    headers.forEach(function(header) {
        headerRow += '<th>' + header + '</th>';
    });
    headerRow += '</tr>';

    // Llenar el cuerpo de la tabla
    let bodyRows = '';
    data.forEach(function(row) {
        bodyRows += '<tr>';
        headers.forEach(function(header) {
            bodyRows += '<td>' + row[header] + '</td>';
        });
        bodyRows += '</tr>';
    });
    let tableHtml = `<thead>${headerRow}</thead><tbody>${bodyRows}</tbody>`;
    document.querySelector(tableId).innerHTML = tableHtml;
}

/*************************************************************************************/

/* FORMATEA Y RENDERIZA EL FORMULARIO DE LOS ALGORITMOS */
const showForm = (elem) => {
    let algKey = elem.value;
    document.querySelector('#algorithm-title').innerText = elem.innerText;
    document.querySelector('#data-model-key').value = algKey;
    let html = `<div class="alg-form-section">
                <label>Seleccione columnas:</label>
                <div class="cols-input-container">`;
    
    let cols = [];

    document.querySelectorAll('#tabla thead tr th').forEach((el) => {
        cols.push(el.innerText);
    })
    
    for(let col of cols){
        html += `<label><input type="checkbox" class="data-cols" name="data-cols" id="${col}" value="${col}"> ${col}</label>`;
    }

    html += `</div></div>
            <div class="alg-form-section">
            <label for="clase-cols-select">Seleccione la columna Clase:  </label>
            <select id="clase-cols-select">
            <option name="data-clase-cols" value="none" selected disabled>-- Seleccione</option>`;
    
    for(let col of cols){
        html += `<option name="data-clase-cols" value="${col}" id="${col}">${col}</option>`;
    }
    
    html += `</select></div>`;
    document.querySelector('#body-alg-form').innerHTML = html;
    
    switch(algKey){
        case 'knn': {
            document.querySelector('#body-alg-form').setAttribute('modo', 'single');
            renderKNNForm();
            break;
        }
        
        case 'kmeans': {
            document.querySelector('#body-alg-form').setAttribute('modo', 'single');
            renderKMeansForm();
            break;
        }
        
        case 'tree': {
            document.querySelector('#body-alg-form').setAttribute('modo', 'multi');
            renderRegtreeForm();
            break;
        }

        case 'regression': {
            document.querySelector('#body-alg-form').setAttribute('modo', 'single');
            renderRegressionForm();
            break;
        }

        default: {
            console.log("Accion no encontrada")
        }
    }

    document.querySelector('#clase-cols-select').addEventListener('change', (e) => {
        document.querySelector('#form-btn-preview').removeAttribute('disabled')
        document.querySelector('#form-btn-process').removeAttribute('disabled')

        document.querySelectorAll('.data-cols:disabled').forEach((elem) => {
            elem.disabled = false;
            elem.checked = false;
            elem.parentElement.style.color = 'initial';
        });
        
        let opcion = e.target.value;
        document.querySelector(`#${opcion}`).checked = true;
        document.querySelector(`#${opcion}`).disabled = true;
        document.querySelector(`#${opcion}`).parentElement.style.color = 'rgb(170,170,170)';
    });

    document.querySelectorAll('.data-cols').forEach((checkbox)=>{
        checkbox.addEventListener('change', ()=>{
            const checkboxesMarcados = document.querySelectorAll('.data-cols:checked:enabled');
            const checkboxesDesmarcados = document.querySelectorAll('.data-cols:not(:checked)');
            
            if(document.querySelector('#body-alg-form').getAttribute('modo') == 'single'){
                if (checkboxesMarcados.length >= 2){
                    for(let cbox of checkboxesDesmarcados){
                        cbox.disabled = true;
                        cbox.parentElement.style.color = 'rgb(170,170,170)';
                    }
                }else{
                    for(let cbox of checkboxesDesmarcados){
                        cbox.disabled = false;
                        cbox.parentElement.style.color = 'initial';
                    }
                }
            }
        });
    });
}

const renderKNNForm = () => {
    document.querySelector('#body-alg-form').innerHTML += `<div class="alg-form-section">
    <label for="k-neighbors-input">Numero de vecinos: </label>
    <input type="number" id="k-neighbors-input" name="k-neighbors-input" value="1" min="1" style="width: 75px; padding: 0 5px">
  </div>
  <div class="alg-form-section">
    <p>Ubicación del centro:</p>
    <label class="ubicacion-ejes-label">Eje X:  <input type="number" id="k-centerx-input" name="k-centerx-input" value="0" min="0" style="width: 75px; padding: 0 5px"></label>
    <label class="ubicacion-ejes-label">Eje Y:  <input type="number" id="k-centery-input" name="k-centery-input" value="0" min="0" style="width: 75px; padding: 0 5px"></label>
  </div>`;
}

const renderKMeansForm = () => {
    document.querySelector('#body-alg-form').innerHTML += `<div class="alg-form-section">
    <label for="k-clusters-input">Numero de clusters: </label>
    <input type="number" id="k-clusters-input" name="k-clusters-input" value="1" min="1" style="width: 75px; padding: 0 5px">
  </div>`;
}

const renderRegtreeForm = () => {
    document.querySelector('#body-alg-form').innerHTML += `<div class="alg-form-section">
    
  </div>`;
}

const renderRegressionForm = () => {
    document.querySelector('#body-alg-form').innerHTML += `<div class="alg-form-section">
    
  </div>`;
}

/*****************************************************/